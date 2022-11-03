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

var SubstituteConnector Strategy

type substituteConnectorStrategy struct {
	connectors map[rune][]string
}

// -----------------------------------------------------------------------------

func (s *substituteConnectorStrategy) Generate(domain, tld string) ([]string, error) {
	res := []string{}
	res = s.permute(res, 0, domain)

	// remove the primary domain from the the list of candidates
	if len(res) > 0 {
		res = res[:len(res)-1]
	}

	return res, nil
}

func (s *substituteConnectorStrategy) permute(permutations []string, index int, curr string) []string {
	if index == len(curr)-1 {
		permutations = append(permutations, curr)
		return permutations
	}

	for i := index; i < len(curr)-1; i++ {
		switch curr[i] {
		case '.':
			for _, connector := range s.connectors['.'] {
				tmp := fmt.Sprintf("%s%s%s", curr[:i], connector, curr[i+1:])
				permutations = s.permute(permutations, i+1, tmp)
			}

		case '-':
			for _, connector := range s.connectors['-'] {
				tmp := fmt.Sprintf("%s%s%s", curr[:i], connector, curr[i+1:])
				permutations = s.permute(permutations, i+1, tmp)
			}

		case '_':
			for _, connector := range s.connectors['_'] {
				tmp := fmt.Sprintf("%s%s%s", curr[:i], connector, curr[i+1:])
				permutations = s.permute(permutations, i+1, tmp)
			}
		}
	}

	permutations = append(permutations, curr)
	return permutations
}

func (s *substituteConnectorStrategy) GetName() string {
	return "SubstituteConnector"
}

func init() {
	SubstituteConnector = &substituteConnectorStrategy{
		connectors: map[rune][]string{
			'.': {"-", "_"},
			'-': {".", "_"},
			'_': {".", "-"},
		},
	}
}
