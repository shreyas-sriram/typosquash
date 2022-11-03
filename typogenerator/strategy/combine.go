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

// var Combine Strategy

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
		res, _ = fuzz(res[0], strategy)
	}

	return res, nil
}

func (s *combineStrategy) GetName() string {
	return "Combine"
}

func fuzz(domain string, strategy Strategy) ([]string, error) {
	res := []string{}
	var err error

	var domains []string
	if strategy != nil {
		domains, err = strategy.Generate(domain, "")

		// Add result
		res = append(res, domains...)
	}

	return res, err
}
