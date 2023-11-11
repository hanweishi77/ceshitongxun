
/**
 * 目标1：信息渲染
 *  1.1 获取用户的数据
 *  1.2 回显数据到标签上
 * */
const creator = 'suifeng';
const head_portrait = localStorage.getItem('head-portrait');
console.log(head_portrait)
head_portrait && (document.querySelector('.prew').src  = `${head_portrait}`)
const p1 =axios({
    url: "/user/info",
    method: 'GET',
    params:{
        creator: 'suifeng',
        imgUrl: head_portrait
    }
});
p1.then((result)=>{
    console.log(result);
    const userObj=result.data;
    console.log(userObj);
    Object.keys(userObj).forEach((key)=>{
      if (key === 'imgUrl') {
         // 赋予默认头像
        document.querySelector('.prew').src = userObj[key];
      } else if (key === 'gender') {
        // 赋予默认性别
        // 获取性别单选框：[男radio元素，女radio元素]
        const gRadioList = document.querySelectorAll('.gender')
        // 获取性别数字：0男，1女
        const gNum = userObj[key]
        // 通过性别数字，作为下标，找到对应性别单选框，设置选中状态
        gRadioList[gNum].checked = true
     } else {
      // 赋予默认内容
      document.querySelector(`.${key}`).value = userObj[key]
     }
    });
})

/**
 * 目标2：修改头像
 *  2.1 获取头像文件
 *  2.2 提交服务器并更新头像
 * */
// 文件选择元素->change事件
document.querySelector('#upload').addEventListener('change', function (e) {
  // 2.1 获取头像文件
  // console.log(e.target.files[0])
  const fd = new FormData()
  fd.append('head-portrait', e.target.files[0])

  // 2.2 提交服务器并更新头像
  axios({
    url: '/user/info',
    method: 'PUT',
    data: fd
  }).then(result => {
      console.log(result)
      const imgUrl = result.data.url
    // 把新的头像回显到页面上,并存储地址于本地
    document.querySelector('.prew').src = imgUrl
    localStorage.setItem('head-portrait', imgUrl)
  })
})
