<template>
<!--  上部新增和搜索-->
  <div class="user-header">
    <el-form :inline="true" ref="formRef" :model="searchForm" label-width="120px" class="demo-form-inline">
      <el-form-item label="Source">
        <el-input v-model="searchForm.source" placeholder="Enter source" />
      </el-form-item>
      <el-form-item label="ProID">
        <el-input v-model="searchForm.proID" placeholder="Enter proID" />
      </el-form-item>
      <el-form-item label="AMP">
        <el-input v-model="searchForm.amp" placeholder="Enter AMP" />
      </el-form-item>
      <el-form-item label="AMP Length">
        <el-input-number v-model="searchForm.amplen" placeholder="Enter AMP length" :min="0" />
      </el-form-item>
      <el-form-item label="Position Start">
        <el-input-number v-model="searchForm.positionStart" placeholder="Enter start position" :min="0" />
      </el-form-item>
      <el-form-item label="Position End">
        <el-input-number v-model="searchForm.positionEnd" placeholder="Enter end position" :min="0" />
      </el-form-item>
      <el-form-item label="Sequence">
        <el-input v-model="searchForm.sequence" placeholder="Enter sequence" />
      </el-form-item>
      <el-form-item label="Pro Clst80">
        <el-input-number v-model="searchForm.pro_clst80" placeholder="Enter Pro Clst80" :min="0" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :disabled="!isValidForm" @click="onSearch">Search</el-button>
        <el-button @click="resetForm">Reset</el-button>
      </el-form-item>
    </el-form>
  </div>
<!--  下部表格-->
  <div class="table">
    <el-table :data="tableData" style="width: 100%">
      <el-table-column
        v-for="item in tableLabel"
        :key="item.prop"
        :width="item.width ? item.width : 125"
        :prop="item.prop"
        :label="item.label"
      />
    </el-table>
    <el-pagination
        class="pager"
        background
        layout="prev, pager, next"
        size="small"
        :total="1000"
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
    prop: "AMPID",
    label: "AMPID",
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
  proID: '',
  amp: '',
  amplen: null,
  positionStart: null,
  positionEnd: null,
  sequence: '',
  pro_clst80: null
})
const formRef = ref(null);

// Computed property to check if at least one field is filled
const isValidForm = computed(() => {
  return Object.values(searchForm).some(value => value !== '' && value !== null);
});

// Handle search button click
const onSearch = () => {
  ElMessage.success("Search submitted with data: " + JSON.stringify(searchForm));
  config.name = searchForm.source
  getUserData()
};

// Reset form to initial state
const resetForm = () => {
  formRef.value.resetFields();
};

//其中total是数据总条数，page是当前的页数，设置name根据name进行条件搜索
const config = reactive({
  total: 5,
  page: 1,
  name: "",
})

const handleChange = (page)=>{
  config.page = page
  getUserData()
}

const getUserData = async () => {
  let data = await proxy.$api.getAllAmpsData(config)
  console.log(data)
  // tableData.value = data.list.map(item=>({   // 注意：本地的mock数据需要用这个
  tableData.value = data.map(item=>({
    ...item,
    // sexLabel : item.sex === "1" ? '男' : '女'
  }))
  // config.total = data.count
}


onMounted(()=>{
  getUserData()
})
</script>


<style lang="less" scoped >
.user-header{
  display: flex;
  justify-content: right;
  .demo-form-inline{
    text-align: right;
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