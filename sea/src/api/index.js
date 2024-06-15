import axios from "axios";

//const baseUrl = 
export const baseUrl = 'http://127.0.0.1:5000'

const httpInstance=axios.create({
    baseURL:'http://127.0.0.1:5000',//配置基准地址
    timeout:5000,  //配置超时时间
	headers:{'Content-Type': 'application/json;charset=utf-8' },
})

export default httpInstance