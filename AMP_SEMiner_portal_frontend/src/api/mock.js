import Mock from 'mockjs'
import allAmpProteinAnimalApi from "@/api/mockData/all_amp_protein_animal.js";

// 1.拦截的路径 2.方法 3 制造出的假数据
Mock.mock(RegExp("/api/getAllAmps" + ".*"), "get", allAmpProteinAnimalApi.getAllAmpsList)
