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
	"fmt"

	"zntr.io/typogenerator/helpers"
)

var Homoglyph Strategy

type homoglyphStrategy struct {
}

// -----------------------------------------------------------------------------

func (s *homoglyphStrategy) Generate(domain, tld string) ([]string, error) {
	res := []string{}
	// `ᅟᅠ         　ㅤǃ！״″＂＄％＆＇﹝（﹞）⁎＊＋‚，‐𐆑－٠۔܁܂․‧。．｡⁄∕╱⫻⫽／ﾉΟοОоՕ𐒆ＯｏΟοОоՕ𐒆Ｏｏا
	// １２３４５６𐒇７Ց８９։܃܄∶꞉：;；‹＜𐆐＝›＞？＠［＼］＾＿｀
	// ÀÁÂÃÄÅàáâãäåɑΑαаᎪＡａßʙΒβВЬᏴᛒＢｂϲϹСсᏟⅭⅽ𐒨ＣｃĎďĐđԁժᎠⅮⅾＤｄÈÉÊËéêëĒēĔĕĖėĘĚěΕЕеᎬＥｅϜＦｆɡɢԌնᏀＧｇʜΗНһᎻＨｈɩΙІіاᎥᛁⅠⅰ𐒃ＩｉϳЈјյᎫＪｊΚκКᏦᛕKＫｋʟιاᏞⅬⅼＬｌΜϺМᎷᛖⅯⅿＭｍɴΝＮｎΟοОоՕ𐒆ＯｏΟοОоՕ𐒆ＯｏΡρРрᏢＰｐႭႳＱｑʀԻᏒᚱＲｒЅѕՏႽᏚ𐒖ＳｓΤτТᎢＴｔμυԱՍ⋃ＵｕνѴѵᏙⅤⅴＶｖѡᎳＷｗΧχХхⅩⅹＸｘʏΥγуҮＹｙΖᏃＺｚ｛ǀا｜｝⁓～ӧӒӦ`
	glyph := map[rune][]string{
		'1': {"１"},
		'2': {"２"},
		'3': {"３"},
		'4': {"４"},
		'5': {"５"},
		'6': {"６"},
		'7': {"𐒇", "７"},
		'8': {"Ց", "&", "８"},
		'9': {"９"},
		'0': {"Ο", "ο", "О", "о", "Օ", "𐒆", "Ｏ", "ｏ", "Ο", "ο", "О", "о", "Օ", "𐒆", "Ｏ", "ｏ"},
		'a': {"à", "á", "â", "ã", "ä", "å", "а", "ɑ", "α", "а", "ａ"},
		'A': {"À", "Á", "Â", "Ã", "Ä", "Å", "Ꭺ", "Ａ"},
		'b': {"d", "lb", "ib", "ʙ", "Ь", "ｂ", "ß"},
		'B': {"ß", "Β", "β", "В", "Ь", "Ᏼ", "ᛒ", "Ｂ"},
		'c': {"ϲ", "с", "ⅽ"},
		'C': {"Ϲ", "С", "с", "Ꮯ", "Ⅽ", "ⅽ", "𐒨", "Ｃ"},
		'd': {"b", "cl", "dl", "di", "ԁ", "ժ", "ⅾ", "ｄ"},
		'D': {"Ꭰ", "Ⅾ", "Ｄ"},
		'e': {"é", "ê", "ë", "ē", "ĕ", "ė", "ｅ", "е"},
		'E': {"È", "É", "Ê", "Ë", "Ē", "Ĕ", "Ė", "Ę", "Ě", "Ε", "Е", "Ꭼ", "Ｅ"},
		'f': {"ｆ"},
		'F': {"Ϝ", "Ｆ"},
		'g': {"q", "ɡ", "Ԍ", "ｇ", "ն"},
		'G': {"Ꮐ", "Ｇ", "Ԍ", "ɢ"},
		'h': {"lh", "ih", "һ", "ｈ"},
		'i': {"j", "ј", "ｊ", "1", "l", "Ꭵ", "ⅰ", "ｉ", "ɩ", "і", "اᎥ", "𐒃"},
		'I': {"Ι", "І", "ᛁ", "Ⅰ", "Ｉ"},
		'j': {"j", "ј", "ｊ", "1", "l", "Ꭵ", "ⅰ", "ｉ", "ϳ", "յ"},
		'J': {"Ј", "ј", "Ꭻ", "Ｊ"},
		'k': {"lk", "ik", "lc", "κ", "ｋ", "κ"},
		'K': {"К", "Ꮶ", "ᛕ", "K", "Ｋ"},
		'l': {"1", "i", "ⅼ", "ｌ", "ӏ", "Ｉ", "ι", "ⅼ", "ｌ"},
		'L': {"ʟ", "اᏞ", "Ⅼ", "Ｌ"},
		'm': {"n", "nn", "rn", "rr", "ⅿ", "ｍ"},
		'M': {"Μ", "Ϻ", "М", "Ꮇ", "ᛖ", "Ⅿ", "Ｍ"},
		'n': {"m", "r", "ｎ", "ɴ"},
		'N': {"ɴ", "Ν", "Ｎ"},
		'o': {"0", "Ο", "ο", "О", "о", "Օ", "𐒆", "Ｏ", "ｏ", "Ο", "ο", "О", "о", "Օ", "𐒆", "Ｏ", "ｏ"},
		'O': {"0", "Ο", "ο", "О", "о", "Օ", "𐒆", "Ｏ", "ｏ", "Ο", "ο", "О", "о", "Օ", "𐒆", "Ｏ", "ｏ"},
		'p': {"ρ", "р", "ｐ", "р"},
		'P': {"Ρ", "Р", "Ꮲ", "Ｐ"},
		'q': {"g", "ｑ"},
		'Q': {"O", "Ⴍ", "Ⴓ", "Ｑ"},
		'r': {"ʀ", "ｒ", "Ի"},
		'R': {"ʀ", "Ꮢ", "ᚱ", "Ｒ"},
		's': {"ѕ", "ｓ"},
		'S': {"Ѕ", "Տ", "Ⴝ", "Ꮪ", "𐒖", "Ｓ"},
		't': {"τ", "ｔ"},
		'T': {"Τ", "Т", "Ꭲ", "Ｔ"},
		'u': {"μ", "υ", "Ս", "Ｕ", "ｕ", "ν"},
		'U': {"Ա", "Ս", "Ｕ"},
		'v': {"ｖ", "ѵ", "ⅴ", "ν"},
		'V': {"Ѵ", "ѵ", "Ꮩ", "Ⅴ", "Ｖ"},
		'w': {"vv", "ѡ", "ｗ", "ѡ"},
		'W': {"Ꮃ", "Ｗ"},
		'x': {"ⅹ", "ｘ", "х"},
		'X': {"Χ", "χ", "Х", "Ⅹ", "Ｘ"},
		'y': {"ʏ", "у", "ｙ"},
		'Y': {"Υ", "γ", "Ү", "Ｙ"},
		'z': {"ｚ"},
		'Z': {"Ζ", "Ꮓ", "Ｚ"},
	}

	dom := []rune(domain)

	for ws := range dom {
		for i := 0; i < (len(dom) - ws); i++ {
			win := dom[i : i+ws]

			j := 0
			for j < ws {
				c := rune(win[j])
				if repList, ok := glyph[c]; ok {
					for _, rep := range repList {
						g := []rune(rep)

						win = []rune(fmt.Sprintf("%s%s%s", string(win[:j]), string(g), string(win[j+1:])))
						if len(g) > 1 {
							j++
						}
						fuzzed := fmt.Sprintf("%s%s%s", string(dom[:i]), string(win), string(dom[i+ws:]))
						fuzzed = combineTLD(fuzzed, tld)
						res = append(res, fuzzed)
					}
				}
				j++
			}
		}
	}

	return helpers.Dedup(res), nil
}

func (s *homoglyphStrategy) GetName() string {
	return "Homoglyph"
}

func init() {
	Homoglyph = &homoglyphStrategy{}
}
