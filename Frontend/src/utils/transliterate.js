const devanagariConsonants = {
  kh: 'ख', gh: 'घ', ch: 'च', jh: 'झ', ph: 'फ', bh: 'भ', th: 'थ', dh: 'ध', sh: 'श', ng: 'ङ',
  k: 'क', g: 'ग', c: 'क', j: 'ज', t: 'ट', d: 'ड', n: 'न', p: 'प', b: 'ब',
  m: 'म', y: 'य', r: 'र', l: 'ल', v: 'व', w: 'व', s: 'स', h: 'ह', f: 'फ', z: 'ज़', x: 'क्स'
}

const devanagariMatras = {
  aa: 'ा', ee: 'ी', ii: 'ी', oo: 'ू', uu: 'ू', ai: 'ै', au: 'ौ',
  a: '', i: 'ि', u: 'ु', e: 'े', o: 'ो'
}

const devanagariIndependentVowels = {
  aa: 'आ', ee: 'ई', ii: 'ई', oo: 'ऊ', uu: 'ऊ', ai: 'ऐ', au: 'औ',
  a: 'अ', i: 'इ', u: 'उ', e: 'ए', o: 'ओ'
}

const malayalamConsonants = {
  kh: 'ഖ', gh: 'ഘ', ch: 'ച', jh: 'ഝ', ph: 'ഫ', bh: 'ഭ', th: 'ഥ', dh: 'ധ', sh: 'ശ', ng: 'ങ',
  k: 'ക', g: 'ഗ', c: 'ക', j: 'ജ', t: 'ട', d: 'ഡ', n: 'ന', p: 'പ', b: 'ബ',
  m: 'മ', y: 'യ', r: 'ര', l: 'ല', v: 'വ', w: 'വ', s: 'സ', h: 'ഹ', f: 'ഫ', z: 'സ്', x: 'ക്സ്'
}

const malayalamMatras = {
  aa: 'ാ', ee: 'ീ', ii: 'ീ', oo: 'ൂ', uu: 'ൂ', ai: 'ൈ', au: 'ൌ',
  a: '', i: 'ി', u: 'ു', e: 'േ', o: 'ോ'
}

const malayalamIndependentVowels = {
  aa: 'ആ', ee: 'ഈ', ii: 'ഈ', oo: 'ഊ', uu: 'ഊ', ai: 'ഐ', au: 'ഔ',
  a: 'അ', i: 'ഇ', u: 'ഉ', e: 'എ', o: 'ഒ'
}

const vowelPatterns = ['aa', 'ee', 'ii', 'oo', 'uu', 'ai', 'au', 'a', 'e', 'i', 'o', 'u']
const consonantPatterns = ['kh', 'gh', 'ch', 'jh', 'ph', 'bh', 'th', 'dh', 'sh', 'ng',
  'k', 'g', 'c', 'j', 't', 'd', 'n', 'p', 'b', 'm', 'y', 'r', 'l', 'v', 'w', 's', 'h', 'f', 'z', 'x']

function matchLongest(str, i, patterns) {
  for (const p of [...patterns].sort((a, b) => b.length - a.length)) {
    if (str.startsWith(p, i)) return p
  }
  return null
}

function transliterateWord(word, consonants, matras, independentVowels) {
  const str = word.toLowerCase()
  let result = ''
  let i = 0
  let expectingConsonant = true

  while (i < str.length) {
    const consMatch = matchLongest(str, i, consonantPatterns)
    const vowelMatch = matchLongest(str, i, vowelPatterns)

    if (consMatch && (!vowelMatch || consMatch.length >= vowelMatch.length || !str.startsWith(vowelMatch, i))) {
      result += consonants[consMatch] || ''
      i += consMatch.length
      
      const nextVowel = matchLongest(str, i, vowelPatterns)
      if (nextVowel) {
        result += matras[nextVowel] ?? ''
        i += nextVowel.length
      }
    } else if (vowelMatch) {
      result += independentVowels[vowelMatch] || ''
      i += vowelMatch.length
    } else {
      result += str[i]
      i += 1
    }
  }
  return result
}

export function transliterateName(name, langCode) {
  if (!name) return name
  if (langCode === 'en') return name

  const scriptMap = {
    hi: { consonants: devanagariConsonants, matras: devanagariMatras, vowels: devanagariIndependentVowels },
    kok: { consonants: devanagariConsonants, matras: devanagariMatras, vowels: devanagariIndependentVowels },
    ml: { consonants: malayalamConsonants, matras: malayalamMatras, vowels: malayalamIndependentVowels }
  }

  const script = scriptMap[langCode]
  if (!script) return name 

  return name
    .split(' ')
    .map(word => transliterateWord(word, script.consonants, script.matras, script.vowels))
    .join(' ')
}