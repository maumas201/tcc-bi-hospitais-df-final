import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import pandas as pd
from serie import obter, MESES, PASTAS
from tccbi.auditoria import conferir_chaves

class Auditoria(unittest.TestCase):
    def setUp(self):
        self.rd=pd.DataFrame([["A","202506","10.00"],["B","202506","20.00"]],columns=["CNES","competencia","VAL_TOT"])
        self.v=pd.DataFrame([["A","202506",1,1000],["B","202506",1,2000]],columns=["CNES","competencia","aih_registros","valor_total_centavos"])
    def test_dois_hospitais(self):
        self.assertEqual(len(conferir_chaves(self.rd,self.v)),2)
    def test_erros_compensados_no_total(self):
        self.v["valor_total_centavos"]=[1100,1900]
        with self.assertRaises(ValueError): conferir_chaves(self.rd,self.v)
    def test_unidade_perdida(self):
        with self.assertRaises(ValueError): conferir_chaves(self.rd,self.v.iloc[:1])
    def test_chave_repetida(self):
        with self.assertRaises(ValueError): conferir_chaves(self.rd,pd.concat([self.v,self.v]))

class Resposta(io.BytesIO):
    def geturl(self): return "ftp://fixture"

class Coleta(unittest.TestCase):
    def test_cobertura_prevista(self):
        self.assertEqual(len({(m,t) for m in MESES for t in PASTAS}),39)
    def test_falha_retomada_e_integridade(self):
        amostra=bytearray(64);amostra[0]=3;amostra[8]=33
        with tempfile.TemporaryDirectory() as temp:
            base=Path(temp)
            with patch("serie.urlopen",side_effect=OSError("indisponível")):
                self.assertEqual(obter(base,"202506","RD","teste",1)["status"],"falha")
            with patch("serie.urlopen",return_value=Resposta(amostra)) as url:
                a=obter(base,"202506","RD","teste",1)
                self.assertEqual(a["status"],"obtido")
                self.assertEqual(obter(base,"202506","RD","teste",1),a)
                self.assertEqual(url.call_count,1)
            (base/"202506"/a["arquivo"]).write_bytes(b"mudou")
            with self.assertRaises(ValueError): obter(base,"202506","RD","teste",1)

class Denominador(unittest.TestCase):
    def test_ausente_e_zero(self):
        from tccbi.core import integrate, prepare
        rd=pd.DataFrame(dict(CNES=["123","456"],ANO_CMPT=["2025"]*2,MES_CMPT=["06"]*2,
                             MUNIC_MOV=["530010"]*2,N_AIH=["1","2"],IDENT=["1"]*2,
                             ESPEC=["1"]*2,DIAS_PERM=["3","6"],VAL_TOT=["100.00","250.00"]))
        st=pd.DataFrame(dict(CNES=["123","456"],COMPETEN=["202506"]*2,CODUFMUN=["530010"]*2))
        lt=pd.DataFrame(dict(CNES=["123"],COMPETEN=["202506"],CODUFMUN=["530010"],
                             TP_LEITO=["1"],CODLEITO=["1"],QT_EXIST=["3"],QT_SUS=["0"]))
        view=integrate(*(prepare(df,t,"202506") for df,t in zip([rd,st,lt],["RD","ST","LT"]))).set_index("CNES")
        self.assertTrue(view.aih_por_leito_sus.isna().all())
        self.assertEqual(view.loc["0000123","leitos_sus"],0)
        self.assertTrue(pd.isna(view.loc["0000456","leitos_sus"]))
        self.assertEqual(view.aih_registros.sum(),2)
