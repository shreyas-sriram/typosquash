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

package main

import (
	"encoding/json"
	"fmt"
	"log"
	"os"

	"github.com/hduplooy/gocsv"
	"github.com/namsral/flag"

	"zntr.io/typogenerator"
	"zntr.io/typogenerator/mapping"
	"zntr.io/typogenerator/strategy"
)

var (
	input      = flag.String("s", "zenithar", "Defines package to alternate")
	JSONOutput = flag.Bool("j", false, "Display JSON output")

	validateCandidates = flag.Bool("v", false, "Perform validation for generated candidates")
)

func init() {
	typogenerator.Registry = flag.String("r", "pypi", "Defines the package registry to search in (rubygems, pypi, npm)")

	flag.Parse()

	if !(*typogenerator.Registry == "pypi" || *typogenerator.Registry == "rubygems" || *typogenerator.Registry == "npm") {
		fmt.Println("Registry can be one of - rubygems, pypi, npm")
		os.Exit(1)
	}
}

func main() {
	all := []strategy.Strategy{
		strategy.Omission,
		strategy.Repetition,
		strategy.Transposition,
		strategy.Prefix,
		strategy.VowelSwap,
		strategy.Replace(mapping.English),
		strategy.DoubleHit(mapping.English),
		strategy.Similar(mapping.English),
		strategy.Suffix,
		strategy.InsertConnector,
		strategy.SubstituteWord,
		strategy.SubstituteConnector,
		strategy.RemoveWord,
		strategy.SwapWord,

		strategy.Combine([]strategy.Strategy{strategy.RemoveWord, strategy.Omission}),

		// strategy.Addition,
		// strategy.BitSquatting,
		// strategy.Homoglyph,
		// strategy.Hyphenation,
		// strategy.SubDomain,
		// strategy.Replace(mapping.French),
		// strategy.DoubleHit(mapping.French),
		// strategy.Similar(mapping.French),
		// strategy.Replace(mapping.Spanish),
		// strategy.DoubleHit(mapping.Spanish),
		// strategy.Similar(mapping.Spanish),
		// strategy.Replace(mapping.German),
		// strategy.DoubleHit(mapping.German),
		// strategy.Similar(mapping.German),
	}

	results, err := typogenerator.Fuzz(*input, all...)
	if err != nil {
		log.Fatal("Unable to generate domains.")
	}

	outputJSON := struct {
		Results []typogenerator.FuzzResult `json:"results"`
	}{
		Results: results,
	}

	if *validateCandidates {
		validPackages := typogenerator.GetValid(results)
		outputJSON = struct {
			Results []typogenerator.FuzzResult `json:"results"`
		}{
			Results: validPackages,
		}
	}

	if !*JSONOutput {
		writer := gocsv.NewWriter(os.Stdout)
		writer.QuoteFields = true
		defer writer.Flush()

		// Write headers
		if err := writer.Write([]string{"strategy", "victim", "candidate"}); err != nil {
			panic(err)
		}

		for _, r := range results {
			for _, p := range r.Permutations {
				if err := writer.Write([]string{r.StrategyName, r.Domain, p.Name}); err != nil {
					panic(err)
				}
			}
		}
	} else {
		b, _ := json.Marshal(outputJSON)
		fmt.Println(string(b))
	}
}
