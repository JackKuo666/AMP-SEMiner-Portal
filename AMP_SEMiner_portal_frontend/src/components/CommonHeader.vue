<template>
  <div class="header">
    <div class="header-left">
      <el-button size="small" @click="handleCollapse">
          <component class="icons" is="menu"></component>
      </el-button>
<!--      <el-breadcrumb separator="/" class="el-breadcrumb">-->
<!--        <el-breadcrumb-item :to="{path: '/'}">首页</el-breadcrumb-item>-->
<!--      </el-breadcrumb>-->
    </div>
<!--    <div class="header-right">-->
<!--      <el-dropdown>-->
<!--        <span class="el-dropdown-link">-->
<!--            <img :src="getImageUrl('user')" class="user"/>-->
<!--        </span>-->
<!--        <template #dropdown>-->
<!--            <el-dropdown-menu>-->
<!--              <el-dropdown-item>个人中心</el-dropdown-item>-->
<!--              <el-dropdown-item>退出</el-dropdown-item>-->
<!--            </el-dropdown-menu>-->
<!--        </template>-->
<!--      </el-dropdown>-->
<!--    </div>-->

  </div>
</template>

<script setup>
import {ref, computed} from "vue"
import {useAllDataStore} from "@/assets/stores/index.js";

const getImageUrl = (user)=>{
  return new URL(`../assets/images/${user}.png`, import.meta.url).href
}
const store = useAllDataStore()
const handleCollapse = () => {
  store.state.isCollapse = !store.state.isCollapse
}

</script>

<style lang="less" scoped>
.header{
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
  background-color: #333333;
}
.icons{
  width: 20px;
  height: 20px;
}
.header-left{
  display: flex;
  align-items: center;
  .el-button{
    margin-right: 20px;
  }
}
.header-right{
  .user{
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
:deep(.bread span){
  color: #ffffff !important;
  cursor: pointer !important;
}
}
</style>