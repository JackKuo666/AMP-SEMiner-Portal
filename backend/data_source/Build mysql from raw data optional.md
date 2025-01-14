# 1.基本操作
注意：以下数据源来自文章，由于建好之后的表已经提供，为了节省github的空间，这里只提供已经建好的表。需要原始数据请联系作者。

## 1.链接数据库
mysql -u root -p

sudo systemctl start mysql // 重启数据库

## 2.mysql 
show databases;
show databases;
+--------------------+
| Database           |
+--------------------+
| amps               |
| anti_defense       |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+

use amps;

show tables;
+----------------+
| Tables_in_amps |
+----------------+
| human_gut_amps |
+----------------+

 SHOW VARIABLES LIKE 'secure_file_priv';
+------------------+-----------------------+
| Variable_name    | Value                 |
+------------------+-----------------------+
| secure_file_priv | /var/lib/mysql-files/ |
+------------------+-----------------------+

// 创建新数据库
CREATE DATABASE my_new_database;

## 3.导入表human_gut_amps
// 创建新tables;
CREATE TABLE human_gut_amps (     AMP_clst INT,     Pro_clst80 INT,     Pro_clst INT,     Source VARCHAR(255),     ProID VARCHAR(255),     ID VARCHAR(255),     Position VARCHAR(255),     AMPlen INT,     AMP VARCHAR(255),     Sequence TEXT,     CID VARCHAR(255),     PDB VARCHAR(255),     DSSP VARCHAR(255),     AMPpdb VARCHAR(255) );

// 新表格导入数据
LOAD DATA INFILE '/var/lib/mysql-files/rmdup.human_gut.clst90_80.AMPclst95.repr_amp_pdb.txt' INTO TABLE human_gut_amps FIELDS TERMINATED BY '\t'   ENCLOSED BY '"'             LINES TERMINATED BY '\n'    IGNORE 1 ROWS;

// 查看表格
describe human_gut_amps;
select * from human_gut_amps limit 2;

// 查看用户
mysql> SELECT CURRENT_USER();
+----------------+
| CURRENT_USER() |
+----------------+
| root@localhost |

// 删除表格
drop table your_table_name 



# 2.导入表all_amp_protein_animal
## 2.1 创建表
```sql
CREATE TABLE all_amp_protein_animal (
    Source VARCHAR(255),
    ProID VARCHAR(255),
    AMP VARCHAR(255),
    AMPlen INT,
    Position VARCHAR(255),
    Sequence TEXT,
    ID VARCHAR(255),
    Pro_clst INT,
    Pro_clst_rep VARCHAR(255),
    Pro_clst80 INT,
    AMPID VARCHAR(255),
    AMP_clst INT,
    seed_ortholog VARCHAR(255),
    evalue DOUBLE,  
    score FLOAT,
    eggNOG_OGs TEXT,
    max_annot_lvl VARCHAR(255),
    COG_category VARCHAR(255),
    Description TEXT,
    Preferred_name VARCHAR(255),
    GOs TEXT,
    EC VARCHAR(255),
    KEGG_ko VARCHAR(255),
    KEGG_Pathway TEXT,
    KEGG_Module TEXT,
    KEGG_Reaction TEXT,
    KEGG_rclass TEXT,
    BRITE VARCHAR(255),
    KEGG_TC VARCHAR(255),
    CAZy VARCHAR(255),
    BiGG_Reaction TEXT,  -- 将 BiGG_Reaction 修改为 TEXT
    PFAMs VARCHAR(255),
    CID VARCHAR(255)  -- 将 CID 也修改为 VARCHAR
);


```

## 2.2 加载数据
```sql
LOAD DATA INFILE '/var/lib/mysql-files/all_amp_protein.animal.clst90_80.AMPclst95.eggnog.txt' 
INTO TABLE all_amp_protein_animal 
FIELDS TERMINATED BY '\t' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(
    Source,
    ProID,
    AMP,
    AMPlen,
    Position,
    Sequence,
    ID,
    Pro_clst,
    Pro_clst_rep,
    Pro_clst80,
    AMPID,
    AMP_clst,
    seed_ortholog,
    @evalue,  
    @score,   
    eggNOG_OGs,
    max_annot_lvl,
    COG_category,
    Description,
    Preferred_name,
    GOs,
    EC,
    KEGG_ko,
    KEGG_Pathway,
    KEGG_Module,
    KEGG_Reaction,
    KEGG_rclass,
    BRITE,
    KEGG_TC,
    CAZy,
    BiGG_Reaction,
    PFAMs,
    CID
)
SET 
    evalue = NULLIF(@evalue, '-'),  --如果它是 '-'，则将 score 列设置为 NULL，否则保留原始值。
    score = NULLIF(@score, '-');   

```


提高检索效率

```
CREATE INDEX idx_amp ON all_amp_protein_animal(AMP);
CREATE INDEX idx_amplen ON all_amp_protein_animal(AMPlen);
CREATE INDEX idx_proclst80 ON all_amp_protein_animal(Pro_clst80);

CREATE INDEX idx_amp_clst ON all_amp_protein_animal(AMP_clst);

```

# 3.导入表 SeqProperties
```
cp /mnt/asustor/wenhui.li/02.AMP/predict/outputs/Token_650M_epoch15/Properties/*Properties.txt /var/lib/mysql-files/
```

```sql
CREATE TABLE SeqProperties (
    `TMPID` VARCHAR(255),
    `AMPlen` INT,
    `AMP` VARCHAR(255),
    `netCharge` FLOAT,
    `molWeight` FLOAT,
    `avgHydro` FLOAT,
    `isoelectricPoint` FLOAT,
    `BomanIndex` FLOAT,
    `Solubility_rules_failed` INT,
    `Synthesis_rules_failed` INT,
    `CrippenLogP` FLOAT,
    `maxHydrophobicMoment` FLOAT,
    `meanHydrophobicMoment` FLOAT,
    `HydrophobicMoment` FLOAT
);

```

```sql
LOAD DATA INFILE '/var/lib/mysql-files/rmdup.human_gut.repr.SeqProperties.txt'  INTO TABLE SeqProperties  FIELDS TERMINATED BY '\t'  ENCLOSEDNCLOSED BY '"'  LINES TERMINATED BY '\n'  IGNORE 1 ROWS (     TMPID,     AMPlen,     AMP,     netCharge,     molWeight,     avgHydro,     isoeelectricPoint,     BomanIndex,     Solubility_rules_failed,     Synthesis_rules_failed,     CrippenLogP,     maxHydrophobicMoment,     meanHyddrophobicMoment,     HydrophobicMoment );
```
```
 SELECT * FROM SeqProperties WHERE AMP = 'LPLTLIRKPIK';
```

# 4.导入表 Pro_StruProperties
```sql
CREATE TABLE Pro_StruProperties (
    ProteinID VARCHAR(255) PRIMARY KEY,
    Rg FLOAT,
    RgNorm FLOAT,
    Area FLOAT,
    AreaPerResi FLOAT,
    MinSemiAxes FLOAT,
    `Loop` FLOAT,        -- 使用反引号包裹保留字
    Coil FLOAT,
    Assort FLOAT,
    `Q` FLOAT,           -- 使用反引号包裹保留字
    Dim FLOAT,
    CVHP FLOAT
);


LOAD DATA INFILE '/var/lib/mysql-files/rmdup.human_gut.repr.Pro_StruProperties.txt'
INTO TABLE Pro_StruProperties
FIELDS TERMINATED BY '\t'  -- 假设字段是由制表符分隔的
ENCLOSED BY '"'            -- 如果有引号包围字段，可指定引号
LINES TERMINATED BY '\n'   -- 每行一个记录
IGNORE 1 LINES;            -- 如果文件第一行是表头，可以忽略

```

# 表5
```sql
CREATE TABLE StruProperties (
    ProteinID VARCHAR(255),
    Rg FLOAT,
    RgNorm FLOAT,
    Area FLOAT,
    AreaPerResi FLOAT,
    MinSemiAxes FLOAT,
    `Loop` FLOAT,        -- 使用反引号包裹
    `Coil` FLOAT,        -- 使用反引号包裹
    Assort FLOAT,
    Q FLOAT,
    Dim FLOAT,
    CVHP FLOAT,
    PRIMARY KEY (ProteinID)
);

LOAD DATA INFILE '/var/lib/mysql-files/rmdup.human_gut.repr.StruProperties.txt'
INTO TABLE StruProperties
FIELDS TERMINATED BY '\t'
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(@proteinID, @Rg, @RgNorm, @Area, @AreaPerResi, @MinSemiAxes, @Loop, @Coil, @Assort, @Q, @Dim, @CVHP)
SET 
  ProteinID = @proteinID, 
  Rg = @Rg,
  RgNorm = @RgNorm,
  Area = @Area,
  AreaPerResi = @AreaPerResi,
  MinSemiAxes = @MinSemiAxes,
  `Loop` = @Loop,
  `Coil` = @Coil,
  Assort = IF(@Assort = '' OR @Assort IS NULL, NULL, @Assort),  -- 将空字符串或NULL替换为NULL
  Q = @Q,
  Dim = @Dim,
  CVHP = IF(@CVHP = '' OR @CVHP IS NULL, NULL, @CVHP);

```
