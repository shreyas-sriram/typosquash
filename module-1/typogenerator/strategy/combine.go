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

package strategy

import "fmt"

type combineStrategy struct {
	strategies []Strategy
}

func Combine(strategies []Strategy) Strategy {
	return &combineStrategy{
		strategies: strategies,
	}
}

// -----------------------------------------------------------------------------

func (s *combineStrategy) Generate(domain, tld string) ([]string, error) {
	res := []string{domain}

	for _, strategy := range s.strategies {
		domains := []string{}
		for _, d := range res {
			fuzzed, _ := fuzz(d, strategy)
			domains = append(domains, fuzzed...)
		}
		res = domains
	}

	return res, nil
}

func (s *combineStrategy) GetName() string {
	name := ""

	for _, s := range s.strategies {
		name = fmt.Sprintf("%s%s, ", name, s.GetName())
	}

	return fmt.Sprintf("Combine(%s)", name[:len(name)-2])
}

func fuzz(domain string, strategy Strategy) ([]string, error) {
	res := []string{}
	var err error

	if strategy != nil {
		domains, err := strategy.Generate(domain, "")
		if err != nil {
			return []string{}, err
		}

		// Add result
		res = append(res, domains...)
	}

	return res, err
}
