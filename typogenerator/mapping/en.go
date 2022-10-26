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

// English mapping
var English Mapping

func init() {
	English = &defaultMapping{
		name: "English",
		keyboard: map[rune][]rune{
			'q': {'1', '2', 'w', 'a'},
			'w': {'2', '3', 'e', 's', 'a', 'q'},
			'e': {'3', '4', 'r', 'd', 's', 'w'},
			'r': {'4', '5', 't', 'f', 'd', 'e'},
			't': {'5', '6', 'y', 'g', 'f', 'r'},
			'y': {'6', '7', 'u', 'h', 'g', 't'},
			'u': {'7', '8', 'i', 'j', 'h', 'y'},
			'i': {'8', '9', 'o', 'k', 'j', 'u'},
			'o': {'9', '0', 'p', 'l', 'k', 'i'},
			'p': {'0', '-', 'l', 'o'},
			'a': {'q', 'w', 's', 'z'},
			's': {'w', 'e', 'd', 'x', 'z', 'a'},
			'd': {'e', 'r', 'f', 'c', 'x', 's'},
			'f': {'r', 't', 'g', 'v', 'c', 'd'},
			'g': {'t', 'y', 'h', 'b', 'v', 'f'},
			'h': {'y', 'u', 'j', 'n', 'b', 'g'},
			'j': {'u', 'i', 'k', 'm', 'n', 'h'},
			'k': {'i', 'o', 'l', 'm', 'j'},
			'l': {'o', 'p', 'k'},
			'z': {'a', 's', 'x'},
			'x': {'s', 'd', 'c', 'z'},
			'c': {'d', 'f', 'v', 'x'},
			'v': {'f', 'g', 'b', 'c'},
			'b': {'g', 'h', 'n', 'v'},
			'n': {'h', 'j', 'm', 'b'},
			'm': {'j', 'k', 'n'},
			'1': {'2', 'q'},
			'2': {'1', '3', 'w', 'q'},
			'3': {'2', '4', 'e', 'w'},
			'4': {'3', '5', 'r', 'e'},
			'5': {'4', '6', 't', 'r'},
			'6': {'5', '7', 'y', 't'},
			'7': {'6', '8', 'u', 'y'},
			'8': {'7', '9', 'i', 'u'},
			'9': {'8', '0', 'o', 'i'},
			'0': {'9', 'p', 'o', '-'},
			'-': {'0', 'p'},
		},
		similar: map[rune][]rune{},
	}
}
