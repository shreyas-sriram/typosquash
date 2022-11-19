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

package strategy_test

import (
	"testing"

	"zntr.io/typogenerator/strategy"
)

// TODO - write better tests
func TestSubstituteConnectorNoConnectors(t *testing.T) {
	out, err := strategy.SubstituteConnector.Generate("zenithar", "")
	if err != nil {
		t.Fail()
		t.Fatal("Error should not occurs !", err)
	}

	expectedCount := 0

	if len(out) != expectedCount {
		t.Errorf("invalid permutation count, expected %d, got %d", expectedCount, len(out))
		t.FailNow()
	}
}

func TestSubstituteConnectorOneConnector(t *testing.T) {
	out, err := strategy.SubstituteConnector.Generate("zeni-thar", "")
	if err != nil {
		t.Fail()
		t.Fatal("Error should not occurs !", err)
	}

	expectedCount := 2

	if len(out) != expectedCount {
		t.Errorf("invalid permutation count, expected %d, got %d", expectedCount, len(out))
		t.FailNow()
	}
}

func TestSubstituteConnectorTwoConnectors(t *testing.T) {
	out, err := strategy.SubstituteConnector.Generate("zen-ith_ar", "")
	if err != nil {
		t.Fail()
		t.Fatal("Error should not occurs !", err)
	}

	expectedCount := 8

	if len(out) != expectedCount {
		t.Errorf("invalid permutation count, expected %d, got %d", expectedCount, len(out))
		t.FailNow()
	}
}

func TestSubstituteConnectorThreeConnectors(t *testing.T) {
	out, err := strategy.SubstituteConnector.Generate("ze_ni-th_ar", "")
	if err != nil {
		t.Fail()
		t.Fatal("Error should not occurs !", err)
	}

	expectedCount := 26

	if len(out) != expectedCount {
		t.Errorf("invalid permutation count, expected %d, got %d", expectedCount, len(out))
		t.FailNow()
	}
}
