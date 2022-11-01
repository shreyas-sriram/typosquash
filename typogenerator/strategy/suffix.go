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

var Suffix Strategy

type suffixStrategy struct {
	suffixes       []string
	simpleSuffixes []string
	connectors     []string
}

// -----------------------------------------------------------------------------

func (s *suffixStrategy) Generate(domain, tld string) ([]string, error) {
	res := []string{}

	for _, suffix := range s.suffixes {
		for _, connector := range s.connectors {
			fuzzed := fmt.Sprintf("%s%s%s", domain, connector, suffix)
			fuzzed = combineTLD(fuzzed, tld)
			res = append(res, fuzzed)
		}
	}

	for _, suffix := range s.simpleSuffixes {
		fuzzed := fmt.Sprintf("%s%s", domain, suffix)
		fuzzed = combineTLD(fuzzed, tld)
		res = append(res, fuzzed)
	}

	return res, nil
}

func (s *suffixStrategy) GetName() string {
	return "Suffix"
}

func init() {
	Suffix = &suffixStrategy{
		suffixes: []string{
			// TODO - add more suffixes
			// Find a way to add `s`, `es` and other plural forms.

			// For suffix `x`, candidates should be generated as:
			// 		foox, foo.x, foo-x, foo_x
			"py",
			"js",
			"1",
			"2",
			"3",
			"v1",
			"v2",
			"v3",
			"cli",
			"core",
			"http",
			"contrib",
			"env",
			"javascript",
			"node",
			"lib",
			"web3",
			"python",
			"api",
			"proxy",
			"plugin",
			"plugins",
			"extend",
			"ext",
			"log",
			"serializable",
			"global",
			"ruby",
			"adapter",
			"main",
			"util",
		},

		connectors: []string{
			"",
			".",
			"-",
			"_",
		},

		simpleSuffixes: []string{
			"s",
			"es",
			"x",
		},
	}
}
