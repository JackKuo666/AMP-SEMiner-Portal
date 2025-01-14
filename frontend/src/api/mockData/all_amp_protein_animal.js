import Mock from 'mockjs'

// get请求从config.url获取参数，post从config.body中获取参数
function param2Obj(url) {
    const search = url.split('?')[1]
    if (!search) {
        return {}
    }
    return JSON.parse(
        '{"' +
        decodeURIComponent(search)
            .replace(/"/g, '\\"')
            .replace(/&/g, '","')
            .replace(/=/g, '":"') +
        '"}'
    )
}

let List = [
    {
        "Source": "ancient_human_gut",
        "ProID": "AZ107.k141_184032_5",
        "AMP": "FRRKKW",
        "AMPlen": 6,
        "Position": "276,281",
        "Sequence": "MQLVLPFEHMAKAAQYMEPSVFEYVREGEIESFESFEKFDFLAFDWYDVHSERTEDYKMLAYVSRENLIIFTEGAAGDTAKKIMDGLAAENPELRSEQLLYRFFVRLLNGDMDCLSRLENEIDEYENVYLFKSESGKDVFEKLSAWRRELLRIKRYYEQLTLIFDEASANDNSVFSNSAAKRFAILKNRTDRYLQTVQNLRDVIEHLQEEYQAQLSIQQNDLMKLFTVVTVIFLPLTLLTGWYGMNFSGMPELNWEYGYLVIIVVSIVVLVALILFFRRKKWL",
        "ID": "ancient_human_gut_AZ107.k141_184032_5",
        "Pro_clst": 1786,
        "Pro_clst_rep": "data_Hadza_ERZ6646243.91_2",
        "Pro_clst80": 52001,
        "AMPID": "ancient_human_gut_AZ107.k141_184032_5:276,281",
        "AMP_clst": 135883,
        "seed_ortholog": "1226322.HMPREF1545_01804",
        "evalue": "1.42e-91",
        "score": 280.0,
        "eggNOG_OGs": "COG0598@1|root,COG0598@2|Bacteria,1TPSV@1239|Firmicutes,24DE3@186801|Clostridia,2N7MM@216572|Oscillospiraceae",
        "max_annot_lvl": "186801|Clostridia",
        "COG_category": "P",
        "Description": "CorA-like Mg2+ transporter protein",
        "Preferred_name": "corA",
        "GOs": "-",
        "EC": "-",
        "KEGG_ko": "ko:K03284",
        "KEGG_Pathway": "-",
        "KEGG_Module": "-",
        "KEGG_Reaction": "-",
        "KEGG_rclass": "-",
        "BRITE": "ko00000,ko02000",
        "KEGG_TC": "1.A.35.1,1.A.35.3",
        "CAZy": "-",
        "BiGG_Reaction": "-",
        "PFAMs": "-"
    },
    {
        "Source": "ancient_human_gut",
        "ProID": "AZ107.k141_604685_1",
        "AMP": "VVGVVSRVTNK",
        "AMPlen": 11,
        "Position": "15,25",
        "Sequence": "MGLNLLLAGLAVLLVVVGVVSRVTNK",
        "ID": "ancient_human_gut_AZ107.k141_604685_1",
        "Pro_clst": 20189,
        "Pro_clst_rep": "ancient_human_gut_AZ107.k141_604685_1",
        "Pro_clst80": 4792,
        "AMPID": "ancient_human_gut_AZ107.k141_604685_1:15,25",
        "AMP_clst": 3954,
        "seed_ortholog": "NoData",
        "evalue": "-",
        "score": "-",
        "eggNOG_OGs": "-",
        "max_annot_lvl": "-",
        "COG_category": "-",
        "Description": "-",
        "Preferred_name": "-",
        "GOs": "-",
        "EC": "-",
        "KEGG_ko": "-",
        "KEGG_Pathway": "-",
        "KEGG_Module": "-",
        "KEGG_Reaction": "-",
        "KEGG_rclass": "-",
        "BRITE": "-",
        "KEGG_TC": "-",
        "CAZy": "-",
        "BiGG_Reaction": "-",
        "PFAMs": "-"
    }
]


export default {
    /**
     * 获取列表
     * 要带参数 name, page, limt; name可以不填, page,limit有默认值。
     * @param name, page, limit
     * @return {{code: number, count: number, data: *[]}}
     */
    getAllAmpsList: (config) => {
        //limit默认是10，因为分页器默认也是一页10个
        const { name, page = 1, limit = 10 } = param2Obj(config.url)

        const mockList = List.filter(user => {
            //如果name存在会，根据name筛选数据
            if (name && user.name.indexOf(name) === -1) return false
            return true
        })
        //分页
        const pageList = mockList.filter((item, index) => index < limit * page && index >= limit * (page - 1))
        return {
            code: 200,
            data: {
                list: pageList,
                count: mockList.length, //数据总条数需要返回
            }
        }
    },
}