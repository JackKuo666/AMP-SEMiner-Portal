<template>
<!--  上部新增和搜索-->
  <div class="user-header">
    <el-form :inline="true" ref="formRef" :model="searchForm" label-width="120px" class="demo-form-inline">
      <el-form-item label="Source">
        <el-input v-model="searchForm.source" placeholder="Enter source" />
      </el-form-item>
      <el-form-item label="AMP Length Min">
        <el-input-number v-model="searchForm.amplenmin"
                         placeholder="Enter AMP Length Min" :min="1" :max="500" />
      </el-form-item>
      <el-form-item label="AMP Length Max">
        <el-input-number v-model="searchForm.amplenmax"
                         placeholder="Enter AMP Length Max"  :min="1" :max="500" />
      </el-form-item>
      <el-form-item label="AMP">
        <el-input
            v-model="searchForm.amp"
            placeholder="Enter AMP"
            style="width: 500px;"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :disabled="!isValidForm" @click="onSearch">Search</el-button>
        <el-button @click="resetForm">Reset</el-button>
      </el-form-item>
    </el-form>
  </div>
<!--  下部表格-->
  <div class="table">
    <el-table :data="tableData" style="width: 100%" @sort-change="handleSortChange">
      <!-- 遍历表格列 -->
      <template v-for="item in tableLabel">
        <!-- 自定义 ProID 列，仅显示前10个字符，鼠标悬停时显示完整内容 -->
        <el-table-column
            v-if="item.prop === 'GOs' || item.prop === 'KEGG_ko' || item.prop === 'KEGG_Pathway'"
            :key="item.prop"
            :width="item.width ? item.width : 150"
            :prop="item.prop"
            :label="item.label"
            sortable
        >
          <template #default="{ row }">
            <el-tooltip
                v-if="row[item.prop] && row[item.prop] !== '-'"
                class="item"
                effect="dark"
                placement="top"
            >
              <!-- 悬浮窗内容 -->
              <template #content>
                <div>
                  <el-link
                      v-for="go in row[item.prop]?.split(',')"
                      :key="go"
                      :href="item.prop === 'GOs' ? `https://www.ebi.ac.uk/QuickGO/GTerm?id=${go}`
                             : `https://www.genome.jp/dbget-bin/www_bget?${go.trim()}`"
                      target="_blank"
                      type="primary"
                      style="margin-right: 5px; display: inline-block;"
                  >
                    {{ go }}
                  </el-link>
                </div>
              </template>
              <!-- 表格中显示简略内容 -->
              <span style="color: #409EFF;">
                {{ row[item.prop] && row[item.prop].length > 10 ? row[item.prop].slice(0, 10) + "..." : row[item.prop] }}
              </span>
            </el-tooltip>
            <span v-else>
              {{ row[item.prop] }}
            </span>
          </template>
        </el-table-column>
        <el-table-column
            v-else-if="item.prop === 'ProID' || item.prop === 'AMP' || item.prop === 'seed_ortholog' "
            :key="item.prop"
            :width="item.width ? item.width : 150"
            :prop="item.prop"
            :label="item.label"
            sortable
        >
          <template #default="{ row }">
            <el-tooltip
                class="item"
                effect="dark"
                :content="row[item.prop]"
                placement="top"
                :style="{ 'max-width': '200px', 'white-space': 'normal', 'word-wrap': 'break-word' }"
            ><!-- 仅显示前10个字符 -->
               <span >
                {{ row[item.prop].length > 10 ? row[item.prop].slice(0, 10) + "..." : row[item.prop] }}
              </span>
            </el-tooltip>
          </template>
        </el-table-column>

        <!-- 自定义 Sequence 列，显示前10个字符并作为超链接 -->
        <el-table-column
            v-else-if="item.prop === 'Sequence'"
            :key="item.prop"
            :width="item.width ? item.width : 125"
            :prop="item.prop"
            :label="item.label"
            sortable
        >
          <template #default="{ row }">
            <el-link
                :underline="false"
                @click="goToGeneInformationPage(row)"
                style="color: #409EFF;"
            >
              <span>{{ row[item.prop].length > 10 ? row[item.prop].slice(0, 10) + "..." : row[item.prop] }}</span>

            </el-link>
          </template>
        </el-table-column>

        <!-- 自定义 Pro_clst80 列，显示为超链接 -->
        <el-table-column
            v-else-if="item.prop === 'Pro_clst80'"
            :key="item.prop"
            :width="item.width ? item.width : 120"
            :prop="item.prop"
            :label="item.label"
            sortable
        >
          <template #default="{ row }">
            <el-link
                :underline="false"
                @click="searchByProClst80(row.Pro_clst80)"
                style="color: #409EFF;"
            >
              {{ row.Pro_clst80 }}
            </el-link>
          </template>
        </el-table-column>

        <!-- 默认显示的其他列 -->
        <el-table-column
            v-else
            :key="item.prop"
            :width="item.prop === 'AMPlen' || item.prop === 'Position' ? 110 : (item.width ? item.width : 150)"
            :prop="item.prop"
            :label="item.label"
            sortable
        />
      </template>
    </el-table>
    <el-pagination
        class="pager"
        background
        layout="prev, pager, next"
        size="small"
        :total="config.total_page"
        @current-change = "handleChange"
    />
  </div>
</template>

<script setup>
import {ref, getCurrentInstance, onMounted, reactive, nextTick, computed} from "vue";
import {ElMessage, ElMessageBox} from "element-plus";


const tableData = ref([])
const {proxy} = getCurrentInstance()
const tableLabel = reactive([
  {
    prop: "Source",
    label: "Source",
  },
  {
    prop: "ProID",
    label: "ProID",
  },
  {
    prop: "AMP",
    label: "AMP",
  },
  {
    prop: "AMPlen",
    label: "AMPlen",
  },
  {
    prop: "Position",
    label: "Position",
  },
  {
    prop: "Sequence",
    label: "Sequence", // 外链：内部
  },
  {
    prop: "Pro_clst80",
    label: "Pro_clst80",
  },
  {
    prop: "AMP_clst",
    label: "AMP_clst",
  },
  {
    prop: "seed_ortholog",  // 链接：外部
    label: "seed_ortholog",
  },
  {
    prop: "GOs",   // 链接：外部
    label: "GOs",
  },
  {
    prop: "KEGG_ko",
    label: "KEGG_ko",
  },
  {
    prop: "KEGG_Pathway",
    label: "KEGG_Pathway",
  },
  {
    prop: "CID",
    label: "CID",
  },
]);


const searchForm = reactive({
  source: '',
  amp: '',
  proClst80: '',
  amplenmin: 1,
  amplenmax: 500,
})
const formRef = ref(null);

// Computed property to check if at least one field is filled
const isValidForm = computed(() => {
  return Object.values(searchForm).some(value => value !== '' && value !== null);
});

// Handle search button click
const onSearch = () => {
  ElMessage.success("Search submitted with data: " + JSON.stringify(searchForm));
  config.source = searchForm.source
  config.amplenmin = searchForm.amplenmin
  config.amplenmax = searchForm.amplenmax
  config.amp = searchForm.amp
  config.proClst80 = NaN
  getUserData()
};

// Reset form to initial state
const resetForm = () => {
  // 刷新页面
  window.location.reload();
};

// 跳转
import { useRouter } from 'vue-router';

const router = useRouter();

const goToGeneInformationPage = async (row) => {
  console.log("sent:", row)
  console.log("config", {tables : "human_gut_amps", source : row.Source, proID : row.ProID, position : row.Position})
    // 调用 API 获取数据
  const response = await proxy.$api.getAllAmpsData( {tables : "human_gut_amps", source : row.Source, proID : row.ProID, position : row.Position});
  console.log("response", response.data);
      // 处理 API 返回的数据
  if (response && response.data.length > 0) {
    row = response.data[0]
  }
  console.log("row", row)

  if (!row) return; // 确保 row 存在
  localStorage.setItem('oneGeneData', JSON.stringify(row)); // 存储 row 数据
  router.push({ name: 'GeneInformationPage' }); // 跳转到 GeneInformationPage
};

// 搜索所有 Pro_clst80 相同的数据
const searchByProClst80 = (proClst80) => {
  ElMessage.success(`Searching for Pro_clst80: ${proClst80}`);
  // 在这里添加实际的搜索逻辑
  searchForm.proClst80 = proClst80; // 将当前 Pro_clst80 设置为搜索条件
  config.proClst80 = proClst80
  getUserData(); // 调用数据获取函数
  // config.proClst80 = NaN
};

//其中total是数据总条数，page是当前的页数，设置name根据name进行条件搜索
const config = reactive({
  tables: 'all_amp_protein_animal',
  proID: '',
  position: '',
  total_page: 100,
  records_per_page: 18,
  page: 1,
  source: '',
  amp: '',
  proClst80: NaN,
  amplenmin: 1,
  amplenmax: 500,
  sortProp: '',
  sortOrder: ''
})

const handleChange = (page)=>{
  config.page = page
  getUserData()
}

const handleSortChange = (sort) => {
  console.log('Sort changed:', sort);
  const { prop, order } = sort; // 获取排序的列和方向
  config.sortProp = prop
  config.sortOrder =   order === 'ascending' ? 'asc' : 'desc'
  if (order) {
    // 根据排序的列和方向调用 API 获取数据
    getUserData();
  }
};

const getUserData = async () => {
  try {
    // 调用 API 获取数据
    const response = await proxy.$api.getAllAmpsData(config);
    console.log("response", response);

    // 处理 API 返回的数据
    if (response && response.data) {
      // 更新表格数据
      tableData.value = response.data.map(item => ({
        ...item,
      }));

      // 更新总记录数
      config.total_page = Math.floor(response.total / config.records_per_page);
      console.log(`Total records: ${config.total_page}`);
    } else {
      console.log("No data returned from the API.");
    }
  } catch (error) {
    console.error("Error fetching user data:", error);
  }
};



onMounted(()=>{
  getUserData()
})
</script>


<style lang="less" scoped >
.user-header{
  display: flex;
  justify-content: right;
  .demo-form-inline{
    text-align: center;
  }
}
.table{
  position: relative;
  height: 95%;
  .el-table{
    width: 100%;
    height: 95%;
  }
  .pager{
    position: absolute;
    right: 10px;
    bottom: auto;
  }
}
.select-clearn{
  display: flex;
}
</style>