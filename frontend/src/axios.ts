import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://127.0.0.1:8081',
})

export default instance