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

var Prefix Strategy

type prefixStrategy struct {
	prefixes   []string
	connectors []string
}

// -----------------------------------------------------------------------------

func (s *prefixStrategy) Generate(domain, tld string) ([]string, error) {
	res := []string{}

	for _, prefix := range s.prefixes {
		for _, connector := range s.connectors {
			fuzzed := fmt.Sprintf("%s%s%s", prefix, connector, domain)
			// fuzzed = combineTLD(fuzzed, tld)
			res = append(res, fuzzed)
		}
	}

	return res, nil
}

func (s *prefixStrategy) GetName() string {
	return "Prefix"
}

func init() {
	Prefix = &prefixStrategy{
		// TODO - add more prefixes
		prefixes: []string{
			"py",
			"python",
			"python3",
			"js",
			"node",
			"jq",
			"async",
			"dev",
			"cli",
			"easy",
			"fast",
			"api",
			"app",
			"ruby",
			"crypto",
			"io",
			"db",
			"stream",
		},

		connectors: []string{
			"",
			".",
			"-",
			"_",
		},
	}
}
