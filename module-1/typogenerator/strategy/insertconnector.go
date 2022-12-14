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

var InsertConnector Strategy

type insertConnectorStrategy struct {
	connectors []string
}

// -----------------------------------------------------------------------------

func (s *insertConnectorStrategy) Generate(domain, tld string) ([]string, error) {
	res := []string{}

	for i := 1; i < len(domain); i++ {
		r := rune(domain[i])
		rp := rune(domain[i-1])
		if !(r == '.' || r == '-' || r == '_') && !(rp == '.' || rp == '-' || rp == '_') {
			for _, connector := range s.connectors {
				fuzzed := fmt.Sprintf("%s%s%s", domain[:i], connector, domain[i:])
				// fuzzed = combineTLD(fuzzed, tld)
				res = append(res, fuzzed)
			}
		}
	}

	return res, nil
}

func (s *insertConnectorStrategy) GetName() string {
	return "InsertConnector"
}

func init() {
	InsertConnector = &insertConnectorStrategy{
		connectors: []string{
			".",
			"-",
			"_",
		},
	}
}
