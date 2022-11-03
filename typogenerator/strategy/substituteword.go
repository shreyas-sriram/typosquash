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

import (
	"strings"
)

var SubstituteWord Strategy

type substituteWordStrategy struct {
	similarWords map[string][]string
}

// -----------------------------------------------------------------------------

func (s *substituteWordStrategy) Generate(domain, tld string) ([]string, error) {
	res := []string{}

	for word, similarWords := range s.similarWords {

		for _, similarWord := range similarWords {
			fuzzed := strings.ReplaceAll(domain, word, similarWord)
			fuzzed = combineTLD(fuzzed, tld)

			if fuzzed != domain {
				res = append(res, fuzzed)
			}
		}
	}

	return res, nil
}

func (s *substituteWordStrategy) GetName() string {
	return "SubstituteWord"
}

func init() {
	SubstituteWord = &substituteWordStrategy{
		similarWords: map[string][]string{
			"python": {"python2", "python3"},

			// TODO - add other words
			// "y": {"ies"},
			// "_": {".", "-"},
		},
	}
}
