// Licensed to Typogenerator under one or more contributor
// license agreements. See the NOTICE file distributed with
// this work for additional information regarding copyright
// ownership. Typogenerator licenses this file to you under
// the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

package typogenerator

import (
	"fmt"
	"io"
	"net/http"
	"strings"
)

var registryURL map[string]string = map[string]string{
	"rubygems": "https://rubygems.org/api/v1/gems/%s.json",
	"pypi":     "https://pypi.org/pypi/%s/json",
	"npm":      "https://registry.npmjs.org/%s",
}

var Registry *string

func normalize(name string) string {
	switch *Registry {
	case "pypi":
		name = strings.ReplaceAll(name, ".", "-")
		name = strings.ReplaceAll(name, "_", "-")
		name = strings.ReplaceAll(name, "--", "-")
	}

	return name
}

func Clean(results []FuzzResult, originalPackage string) []FuzzResult {
	var cleanedResults []FuzzResult
	seen := map[string]bool{originalPackage: true}

	for _, result := range results {
		cleanedPermutations := []Permutation{}
		for _, permutation := range result.Permutations {
			candidateName := permutation.Name

			candidateName = normalize(candidateName)

			_, ok := seen[candidateName]
			if !ok {
				permutation.Name = candidateName
				cleanedPermutations = append(cleanedPermutations, permutation)
				seen[candidateName] = true
			}
		}
		result.Permutations = cleanedPermutations
		cleanedResults = append(cleanedResults, result)
	}

	return cleanedResults
}

func GetValid(results []FuzzResult) []FuzzResult {
	validPackages := []FuzzResult{}

	// rubygems API throttles requests, hence no concurrrency.
	// pypi and npm are good.
	if *Registry == "rubygems" {
		for _, r := range results {
			for _, p := range r.Permutations {
				if exists(p.Name, *Registry) {
					validPackages = append(validPackages, FuzzResult{StrategyName: r.StrategyName, Domain: r.Domain, Permutations: []Permutation{{p.Name, true}}})
				}
			}
		}
	} else {
		ch := make(chan FuzzResult)

		total := 0

		for _, r := range results {
			total += len(r.Permutations)
			for _, p := range r.Permutations {
				go func(p string, r FuzzResult) {
					if exists(p, *Registry) {
						ch <- FuzzResult{StrategyName: r.StrategyName, Domain: r.Domain, Permutations: []Permutation{{p, true}}}
					} else {
						ch <- FuzzResult{StrategyName: r.StrategyName, Domain: r.Domain, Permutations: []Permutation{{p, false}}}
					}
				}(p.Name, r)
			}
		}

		for i := 0; i < total; i++ {
			select {
			case resp := <-ch:
				if resp.Permutations[0].Valid {
					validPackages = append(validPackages, resp)
				}
			}
		}
	}

	return validPackages
}

func exists(packageName, registry string) bool {
	URL := fmt.Sprintf(registryURL[registry], packageName)

	return makeRequest(URL)
}

func makeRequest(URL string) bool {
	resp, err := http.Get(URL)

	if err != nil {
		return false
	}

	defer resp.Body.Close()

	if resp.StatusCode == http.StatusNotFound {
		return false
	}

	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return false
	}

	// handle old npm security handles - https://www.npmjs.com/package/axois
	if strings.Contains(string(b), "security holding package") {
		return false
	}

	return true
}
