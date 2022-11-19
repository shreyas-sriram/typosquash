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
	"github.com/weppos/publicsuffix-go/publicsuffix"

	"zntr.io/typogenerator/strategy"
)

type Permutation struct {
	Name  string `json:"name" yaml:"name"`
	Valid bool   `json:"valid" yaml:"valid"`
}

// FuzzResult represents permutations results
type FuzzResult struct {
	StrategyName string        `json:"strategy" yaml:"strategy"`
	Domain       string        `json:"package_name" yaml:"package_name"`
	Permutations []Permutation `json:"candidate" yaml:"candidate"`
}

// Fuzz string using given strategies
func Fuzz(name string, strategies ...strategy.Strategy) ([]FuzzResult, error) {
	return fuzz(name, "", strategies...)
}

// FuzzDomain splits a domain into (TRD + SLD) + TLD and fuzzes using given strategies
func FuzzDomain(domain string, strategies ...strategy.Strategy) ([]FuzzResult, error) {
	parsed, err := publicsuffix.Parse(domain)
	if err != nil {
		return []FuzzResult{}, err
	}

	domain = parsed.SLD
	if parsed.TRD != "" {
		domain = parsed.TRD + "." + domain
	}

	return fuzz(domain, parsed.TLD, strategies...)
}

func fuzz(domain, tld string, strategies ...strategy.Strategy) ([]FuzzResult, error) {
	res := []FuzzResult{}
	var err error

	var domains []string
	for _, s := range strategies {
		if s != nil {
			r := FuzzResult{
				StrategyName: s.GetName(),
				Domain:       domain,
			}

			domains, err = s.Generate(domain, tld)
			if err != nil {
				break
			}

			// Assign permutations to result
			for _, d := range domains {
				r.Permutations = append(r.Permutations, Permutation{d, false})
			}

			// Add result
			res = append(res, r)
		}
	}

	return res, err
}
