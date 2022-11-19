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

package mapping

// French mapping
var French Mapping

func init() {
	French = &defaultMapping{
		name: "French",
		keyboard: map[rune][]rune{
			'a': {'1', '2', 'z', 'q', 'é'},
			'z': {'2', '3', 'e', 'é', 's', 'a', 'q'},
			'e': {'3', '4', 'r', 'd', 's', 'z'},
			'r': {'4', '5', 't', 'f', 'd', 'e'},
			't': {'5', '6', 'y', 'g', 'f', 'r', '-'},
			'y': {'6', '7', 'u', 'h', 'g', 't', 'è', '-'},
			'u': {'7', '8', 'i', 'j', 'h', 'y', 'è'},
			'i': {'8', '9', 'o', 'k', 'j', 'u', 'ç'},
			'o': {'9', '0', 'p', 'l', 'k', 'i', 'ç', 'à'},
			'p': {'0', 'à', 'l', 'o'},
			'q': {'a', 'z', 's', 'w'},
			's': {'z', 'e', 'd', 'x', 'w', 'q'},
			'd': {'e', 'r', 'f', 'c', 'x', 's'},
			'f': {'r', 't', 'g', 'v', 'c', 'd'},
			'g': {'t', 'z', 'h', 'b', 'v', 'f'},
			'h': {'z', 'u', 'j', 'n', 'b', 'g'},
			'j': {'u', 'i', 'k', 'm', 'n', 'h'},
			'k': {'i', 'o', 'l', 'm', 'j'},
			'l': {'o', 'p', 'm', 'k'},
			'm': {'p', 'ù', 'l'},
			'w': {'q', 's', 'x'},
			'x': {'s', 'd', 'c', 'w'},
			'c': {'d', 'f', 'v', 'x'},
			'v': {'f', 'g', 'b', 'c'},
			'b': {'g', 'h', 'n', 'v'},
			'n': {'h', 'j', 'b'},
			'1': {'2', 'a', 'é'},
			'2': {'1', '3', 'a', 'z', 'é'},
			'3': {'2', '4', 'e', 'w', 'é'},
			'4': {'3', '5', 'r', 'e'},
			'5': {'4', '6', 't', 'r'},
			'6': {'5', '7', 'y', 't', 'è'},
			'7': {'6', '8', 'u', 'y', 'è'},
			'8': {'7', '9', 'i', 'u', 'è', 'ç'},
			'9': {'8', '0', 'o', 'i', 'ç', 'à'},
			'0': {'9', 'à', 'ç', 'p', 'o'},
		},
		similar: map[rune][]rune{
			'a': {'à', 'â', 'ä'},
			'à': {'a', 'â', 'ä'},
			'â': {'à', 'a', 'ä'},
			'ä': {'à', 'â', 'a'},
			'e': {'è', 'é', 'ê', 'ë'},
			'è': {'e', 'é', 'ê', 'ë'},
			'é': {'è', 'e', 'ê', 'ë'},
			'ê': {'é', 'è', 'e', 'ë'},
			'ë': {'é', 'è', 'ê', 'e'},
			'i': {'î', 'ï'},
			'î': {'i', 'ï'},
			'ï': {'î', 'i'},
			'u': {'ù', 'ü', 'û'},
			'ù': {'u', 'ü', 'û'},
			'ü': {'ù', 'u', 'û'},
			'û': {'ù', 'ü', 'u'},
			'o': {'ö', 'ô'},
			'ö': {'o', 'ô'},
			'ô': {'ö', 'o'},
			'y': {'ÿ', 'ŷ'},
			'ÿ': {'y', 'ŷ'},
			'ŷ': {'ÿ', 'y'},
			'c': {'ç'},
			'ç': {'c'},
		},
	}
}
