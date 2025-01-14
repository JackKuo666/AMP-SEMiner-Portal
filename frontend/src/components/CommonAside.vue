<template>
  <el-aside :width="width">
    <el-menu
      background-color="#545c64"
      text-color="#ffff"
      :collapse="isCollapse"
      :collapse-transition="false"
    >
      <h3 v-show="!isCollapse">MAG-AMPome</h3>
      <h3 v-show="isCollapse">MAG</h3>
      <el-menu-item
        v-for="item in noChildren"
        :index="item.path"
        :key="item.path"
        @click="clickMenu(item)"
      >
          <component class="icons" :is="item.icon"></component>
          <span>{{item.label}}</span>
      </el-menu-item>
      <el-sub-menu
          v-for="item in hasChildren"
          :index="item.path"
          :key="item.path"
      >
        <template #title>
          <component class="icons" :is="item.icon"></component>
          <span>{{item.label}}</span>
        </template>
        <el-menu-item-group>
          <el-menu-item
              v-for="(subItem, subIndex) in item.children"
              :index="subItem.path"
              :key="subItem.path"
              @click="clickMenu(subItem)"
          >
            <component class="icons" :is="subItem.icon"></component>
            <span>{{subItem.label}}</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-sub-menu>
    </el-menu>
  </el-aside>
</template>

<script setup>
import {ref, computed} from "vue"
import {useAllDataStore} from "@/assets/stores/index.js";

const list = ref([
  {
    path: '/home',
    name: 'home',
    label: 'Home',
    icon: 'house',
    url: 'Home'
  },
  {
    path: '/browse',
    name: 'mall',
    label: 'Browse',
    icon: 'search',
    url: 'Browse'
  },
  {
    path: '/download',
    label: 'Download',
    icon: 'download',
    url: 'Download'
  },
  {
    path: '/help',
    name: 'Help',
    label: 'Help',
    icon: 'user',
    url: 'Help'
  }
])

const noChildren = computed(() => list.value.filter(item => !item.children))
const hasChildren =computed(() => list.value.filter(item => item.children))
const store = useAllDataStore()
const isCollapse = computed(() => store.state.isCollapse)
//width
const width = computed(() => store.state.isCollapse ? '64px' : '180px')
import {useRouter, useRoute} from "vue-router";
const router = useRouter()

const clickMenu=(item)=>{
  router.push(item.path)
}
</script>

<style lang="less" scoped>

.icons{
  width:18px;
  height:18px;
  margin-right:5px;
}
.el-menu{
  border-right:none;
  h3{
    line-height:48px;
    color:#fff;
    text-align:center;
  }
}
.el-aside{
  height:100%;
  background-color:#545c64;
}
</style>