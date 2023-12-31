# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['SocioEco.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['srsly.msgpack.util', 'cymen', 'thinc', 'srsly', 'requests', 'plac', 'preshed', 'wasabi', 'cymem', 'murmurhash', 'blis','cymem.cymem', 'preshed.maps', 'thinc.linalg', 'thinc.neural._aligned_alloc', 'blis.py', 'spacy.strings', 'pkg_resources.py2_warn', 'spacy.morphology','thinc.extra.search','spacy._align','spacy.matcher.dependencymatcher','spacy.syntax.nonproj','spacy.language','spacy.cli.debug_data','spacy.tokens','spacy.matcher.matcher','spacy.cli.download','spacy.lang.en.tag_map','spacy.displacy.templates','spacy.lang.en.lemmatizer._adverbs_irreg','spacy.pipeline','spacy.cli.converters.conll_ner2json','spacy.about','spacy.cli.pretrain','spacy.lang.en.lemmatizer._adjectives_irreg','spacy._ml','spacy.gold','spacy.tokens.token','spacy.lang.en.lemmatizer','spacy.matcher.phrasematcher','spacy.lang.en.tokenizer_exceptions','spacy.cli.link','spacy.displacy.render','spacy.lang.en.lemmatizer._adverbs','spacy.lang.en.morph_rules','spacy.cli.profile','spacy.cli.train','spacy.pipeline.hooks','spacy.lang.en.lemmatizer._verbs_irreg','spacy.cli.info','spacy.glossary','spacy.attrs','spacy.lang.en.syntax_iterators','spacy.compat','spacy.lang.tokenizer_exceptions','spacy.tokens.underscore','spacy.lang.en','spacy.symbols','spacy.pipeline.entityruler','spacy.syntax.arc_eager','spacy.vectors','spacy.lang.en.lemmatizer._nouns_irreg','spacy.matcher._schemas','spacy.pipeline.pipes','spacy.lang','spacy.errors','spacy.syntax.transition_system','spacy.lang.char_classes','spacy.cli.init_model','spacy.tokenizer','spacy.cli','spacy.lang.en.lex_attrs','spacy.lang.norm_exceptions','spacy.cli.evaluate','spacy.pipeline.functions','spacy.lexeme','spacy.lang.en.lemmatizer.lookup','spacy.syntax._beam_utils','spacy.util','spacy.cli.convert','spacy.syntax._parser_model','spacy.lang.en.norm_exceptions','spacy','spacy.cli.validate','spacy.parts_of_speech','spacy.vocab','spacy.cli.converters.conllu2json','spacy.cli.converters.iob2json','spacy.morphology','spacy.tokens._retokenize','spacy.kb','spacy.lang.en.stop_words','spacy.syntax.stateclass','spacy.syntax','spacy.lang.en.lemmatizer._lemma_rules','spacy.lang.en.lemmatizer._verbs','spacy.lang.punctuation','spacy.cli.package','spacy.scorer','spacy.cli.converters.jsonl2json','spacy.lang.en.lemmatizer._nouns','spacy.lang.en.lemmatizer._adjectives','spacy.cli.converters','spacy.tokens.doc','spacy.syntax.ner','spacy.lang.tag_map','spacy.matcher','spacy.lemmatizer','spacy.strings','spacy.tokens.span','spacy.displacy','spacy.syntax.nn_parser','spacy.lang.lex_attrs'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SocioEco',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
