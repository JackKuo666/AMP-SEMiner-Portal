import {defineStore} from "pinia";
import {ref} from "vue"
function initState(){
    return{
        isCollapse: false,
    }
}

export const useAllDataStore = defineStore("AllData", () =>{
    // ref state 属性
    // computed getters
    // function actions
    const state = ref(initState());
    return {
        state
    }
    }

)