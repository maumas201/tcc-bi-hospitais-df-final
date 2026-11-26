"""Mede AppTest da revisao avaliada; nao mede renderizacao do navegador.
Uso: python medir_desempenho_tcc.py CAMINHO_VERSAO_AVALIADA PASTA_SAIDA
"""
import argparse
import csv
import datetime as dt
import importlib.metadata as md
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

COMMIT = '09f2817ca8a9d60fe1cfa21656f9b7f8a931a76b'
OPERACOES = ('primeira_execucao_apptest', 'filtro_competencia', 'filtro_estabelecimento')


def worker(versao, saida, rodada):
    from streamlit.testing.v1 import AppTest
    app = AppTest.from_file(str(versao / 'app.py'), default_timeout=60)
    registros = []

    def medir(operacao, executar, esperado):
        inicio = time.perf_counter()
        executar()
        duracao = time.perf_counter() - inicio
        observado = [m.value for m in app.metric][:2]
        sucesso = not bool(app.exception) and observado == esperado
        registros.append({'rodada': rodada, 'operacao': operacao,
                          'segundos': f'{duracao:.6f}', 'esperado': ' | '.join(esperado),
                          'observado': ' | '.join(str(x) for x in observado),
                          'situacao': 'APROVADO' if sucesso else 'FALHOU'})
        saida.write_text(json.dumps(registros, ensure_ascii=False, indent=2), encoding='utf-8')
        if not sucesso:
            raise RuntimeError(f'{operacao}: esperado {esperado!r}, observado {observado!r}; excecoes={app.exception!r}')

    medir(OPERACOES[0], app.run, ['265.907', 'R$ 469.282.753,25'])
    medir(OPERACOES[1], lambda: app.select_slider[0].set_value(('202506', '202506')).run(),
          ['21.120', 'R$ 33.972.979,19'])
    medir(OPERACOES[2], lambda: app.selectbox[0].select('0010456').run(),
          ['2.511', 'R$ 7.590.382,95'])


def principal(versao, saida):
    commit = subprocess.check_output(['git', '-C', str(versao), 'rev-parse', 'HEAD'], text=True).strip()
    if commit != COMMIT:
        raise SystemExit(f'Revisao incorreta: {commit}. Esperado: {COMMIT}')
    status = subprocess.check_output(['git', '-C', str(versao), 'status', '--porcelain', '--untracked-files=no'], text=True).strip()
    if status:
        raise SystemExit('Ha alteracoes em arquivos versionados. Preserve-as e use uma copia limpa da revisao avaliada.')
    saida.mkdir(parents=True, exist_ok=False)
    meta = {'inicio': dt.datetime.now().astimezone().isoformat(), 'commit': commit,
            'python': sys.version, 'sistema': platform.platform(),
            'dependencias': {p: md.version(p) for p in ('streamlit', 'pandas', 'altair')},
            'protocolo': '3 processos Python separados, primeira chamada AppTest.run e dois filtros sequenciais no mesmo AppTest; tempo perf_counter; sem navegador; importacao do AppTest e inicio do processo excluidos; cache de disco do SO nao controlado.',
            'parametros': {'periodo_inicial': '202506-202606', 'filtro_competencia': '202506', 'filtro_cnes': '0010456'}}
    (saida / 'metodo.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    registros = []
    falha = False
    for rodada in range(1, 4):
        arquivo = saida / f'rodada_{rodada}.json'
        cmd = [sys.executable, str(Path(__file__).resolve()), str(versao), str(arquivo), '--rodada', str(rodada)]
        p = subprocess.run(cmd, cwd=versao, capture_output=True)
        (saida / f'rodada_{rodada}.log').write_bytes(p.stdout + b'\n--- STDERR ---\n' + p.stderr + f'\ncodigo_saida={p.returncode}\n'.encode())
        if arquivo.exists():
            registros.extend(json.loads(arquivo.read_text(encoding='utf-8')))
        print(f'Rodada {rodada}: codigo_saida={p.returncode}', flush=True)
        if p.returncode != 0:
            falha = True
            break
    with (saida / 'desempenho.csv').open('w', encoding='utf-8-sig', newline='') as arq:
        w = csv.DictWriter(arq, fieldnames=['rodada','operacao','segundos','esperado','observado','situacao'], delimiter=';')
        w.writeheader(); w.writerows(registros)
    resumo = []
    for op in OPERACOES:
        dados = [float(r['segundos']) for r in registros if r['operacao'] == op and r['situacao'] == 'APROVADO']
        if len(dados) == 3:
            resumo.append({'operacao': op, 'n': 3, 'mediana_segundos': round(statistics.median(dados), 6), 'min_segundos': min(dados), 'max_segundos': max(dados)})
    (saida / 'resumo.json').write_text(json.dumps(resumo, indent=2), encoding='utf-8')
    print(json.dumps(resumo, indent=2), flush=True)
    print(f'Evidencias: {saida}', flush=True)
    return 1 if falha or len(registros) != 9 else 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('versao', type=Path)
    parser.add_argument('saida', type=Path)
    parser.add_argument('--rodada', type=int)
    args = parser.parse_args()
    if args.rodada is not None:
        worker(args.versao.resolve(), args.saida.resolve(), args.rodada)
    else:
        sys.exit(principal(args.versao.resolve(), args.saida.resolve()))
