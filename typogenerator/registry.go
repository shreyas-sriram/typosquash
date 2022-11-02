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
	"fmt"
	"net/http"
)

var registryURL map[string]string = map[string]string{
	"rubygems": "https://rubygems.org/api/v1/gems/%s.json",
	"pypi":     "https://pypi.org/pypi/%s/json",
	"npm":      "https://registry.npmjs.org/%s",
}

func Exists(packageName, registry string) bool {
	URL := fmt.Sprintf(registryURL[registry], packageName)

	return exists(URL)
}

func exists(URL string) bool {
	resp, err := http.Get(URL)
	if err != nil || resp.StatusCode == http.StatusNotFound {
		return false
	}

	defer resp.Body.Close()

	return true
}
