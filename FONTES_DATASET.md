# 📦 Fontes do dataset do projeto — Online Retail

O dataset oficial do curso é o **Online Retail** (vendas de uma loja online do Reino
Unido, dez/2010–dez/2011, ~541 mil linhas) — o mesmo usado no guia oficial
*Spark: The Definitive Guide*. **Schema** (bate com os notebooks):

```
InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country
```

## ✅ Fontes verificadas (em ordem de preferência)

### 1. Dataset local do Databricks (recomendado — roda na Free Edition sem internet)
O workspace do Databricks já fornece o arquivo. Os notebooks tentam, em ordem:

| Caminho | Quando existe |
|---|---|
| `/databricks-datasets/online-retail-dataset/data-original/online-retail-dataset.csv` | workspaces com os sample datasets montados em DBFS |
| `/Volumes/samples/databricks/datasets/online_retail/online_retail.csv` | workspaces com o catálogo `samples` (Unity Catalog) |

Liste o que existe no seu workspace:
```python
display(dbutils.fs.ls("/databricks-datasets"))
# ou
LIST '/Volumes/samples/databricks/datasets/'
```

### 2. GitHub oficial do Databricks (fallback, precisa de internet)
- Repositório: https://github.com/databricks/Spark-The-Definitive-Guide
- Arquivo: `data/retail-data/all/online-retail-dataset.csv`
- Raw (usado nos notebooks):
  `https://raw.githubusercontent.com/databricks/Spark-The-Definitive-Guide/master/data/retail-data/all/online-retail-dataset.csv`
- **Verificado**: HTTP 200, ~45 MB, 541.909 linhas + cabeçalho.

### 3. UCI Machine Learning Repository (origem original)
- Página: https://archive.ics.uci.edu/dataset/352/online+retail
- Arquivo: `Online Retail.xlsx` (formato Excel — requer conversão para CSV).

### 4. Kaggle (requer conta)
- https://www.kaggle.com/datasets/laurentian120/online-retail (e outras cópias).
- Cuidado: versões do Kaggle podem ter colunas extras/limpeza diferente — use
  apenas se as colunas batem com o schema acima.

## 🔁 Como os notebooks carregam

1. Tentam o **dataset local do Databricks** (célula 1) → copiam para `/FileStore/vendas.csv`.
2. Se não achar, fazem **download do raw do GitHub oficial** (célula 2) → mesmo destino.
3. Se ambos falharem, o notebook instrui o **upload manual**:
   baixe o CSV (fontes 2/3/4) e use **Data → Add Data → Upload File** (destino `/FileStore`).

## 📚 Sobre os dados sintéticos (voos)

A tabela `workspace.bronze.voos_bronze` é **gerada pelo próprio notebook** (Semana 1,
Dia 5) com `random.seed(42)` — não depende de download.
