document.querySelector('.test-btn').addEventListener('click', function () {
    axios({
        url: '/book/list',
        method: 'post',
        params: {
            creator: '老李'
        }
    }).then(result =>{
        console.log(result.data)
    })
});