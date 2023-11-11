

// 1.查询渲染图书列表
function renderBookList(creator) {
	const list =document.querySelector('.table .list');
	axios({
	  url: "/book/list",
	  method: "GET",
	  params:{
	    creator: creator
	  }
	}).then(function(result) {
	console.log(result);
	const bookList = result.data;
	let str = '';
	bookList.forEach(item=>{
		const {author,bookname,id,publisher}=item;
		str +=`<tr><td>${id}</td><td>${bookname}</td>
				<td>${author}</td>
          <td>${publisher}</td>
          <td>
            <span class="del">删除</span>
            <span class="edit">编辑</span>
          </td>
        </tr>
		`;
	});
	list.innerHTML=str;
	})
}
const creator = '老李';
renderBookList(creator);


//2. 添加图书功能
/**
 * 目标：新增图书
 *  1 弹框->显示和隐藏
 *  2 收集表单数据，并提交到服务器保存
 *  3 刷新图书列表
 */
// 2.1 创建弹框的bootstrap对象,可调用hide show方法
const bookModalDom = document.querySelector('#book-edit');
const bookModal = new bootstrap.Modal(bookModalDom);
// 2.2 添加按钮的提交事件
document.querySelector('#book-edit .save-btn').addEventListener('click', function(e){
	// 获取表单对象
	const bookForm = document.querySelector("#book-edit .book-edit");
	// 获取表单name条目的 value
	const data = serialize(bookForm, { hash: true, empty: true });
	// console.log(data);
	// 对象解构
	const {bookname,author,item} = data;
	// axios发送数据
	axios({
		url:'/book/list',
		method:'post',
		data:{
			bookname:bookname,
			author:author,
			publisher:item,
			creator:creator
		}
	}).then(function(res) {
		// console.log(res.data.message);
		// 提交成功，重新渲染图书列表
		renderBookList(creator);
		// 重置表单
		bookForm.reset();
		// 关闭弹框
		bookModal.hide();
	}).catch(error =>{
		 // console.log(error);
		 alert(error.response.data.message);
	})
	
})


/**
 * 目标3：删除图书
 *  1 删除元素绑定点击事件->获取图书id
 *  2 调用删除接口
 *  3 刷新图书列表
 */
// 3 删除图书
//3.1 创建图书列表对象 事件委托注册点击事件
const list =document.querySelector('.table .list');

list.addEventListener('click', function(e) {
	// console.log(e.target);
	// 如果是删除按钮
	if(e.target.classList.contains('del')){
		// 获取图书的id    childNodes子节点会包括文本节点等，容易出错
		// console.log(e.target.parentNode.parentNode.childNodes[0].innerText);
		const bookId = e.target.parentNode.parentNode.childNodes[0].innerText;
		// axios发送数据
			axios({
				url:`/book/list/${bookId}`,
				method:'delete',
			}).then(function(res) {
				// console.log(res.data.message);
				// 刷新图书列表
				renderBookList(creator);
			}).catch(error =>{
				 // console.log(error);
				 alert(error.response.data.message);
			})
	}

});


/**
 * 目标4：修改图书
 *  1 编辑弹框->显示和隐藏
 *  2 获取当前编辑图书数据->回显到编辑表单中
 *  3 提交保存修改，并刷新列表
 */
// 4.1 修改弹框->显示和隐藏
//     创建弹框的bootstrap对象,可调用hide show方法
const bookModifyModalDom = document.querySelector('#book-modify');
const bookModifyModal = new bootstrap.Modal(bookModifyModalDom);
//  创建图书列表对象list在目标3已创建
list.addEventListener('click', function(e) {
	// console.log(e.target);
	// 如果是编辑按钮
	if(e.target.classList.contains('edit')){
		// 弹出编辑框
		 bookModifyModal.show();
		//4.2 取接口数据，填充编辑框内容
		const bookId = e.target.parentNode.parentNode.childNodes[0].innerText;
		// axios请求图书详情数据
			axios({
				url:`/book/list/${bookId}`,
				method:'get',
			}).then(function(res) {
				console.log(res.data);
				// 接收图书详情数据
				const {bookname, publisher, author,id}= res.data;
				// console.log(bookname);
				// 填充编辑框
				document.querySelector('#book-modify input[name="bookname"]').value=bookname;
				document.querySelector('#book-modify input[name="author"]').value=author;
				document.querySelector('#book-modify input[name="item"]').value=publisher;
				document.querySelector('#book-modify input[name="id"]').value=id;
				// console.log(document.querySelector('#book-modify input[name="id"]').value);
			}).catch(error =>{
				 // console.log(error);
				 alert(error.response.data.message);
			})
	}
	
});

// 4.3编辑弹框修改按钮->点击->隐藏弹框，提交修改
document.querySelector('#book-modify .edit-btn').addEventListener('click', function(){
	// 获取修改的数据
	modifyForm = document.querySelector('#book-modify .book-edit');
	console.log(document.querySelector('#book-modify input[name="id"]').value);
	const data = serialize(modifyForm, { hash: true, empty: true })
	// console.log(data);
	const { bookname, item, author}=data;
	const bookId = document.querySelector('#book-modify input[name="id"]').value;
	console.log(bookname, item, author,bookId);
	// axios发送修改数据
		axios({
			url:`/book/list/${bookId}`,
			method:'put',
			data: {
				bookname: bookname,
				author: author,
				publisher: item,
				creator:creator
			}
		}).then(function(res) {
			console.log(res.data.message);
			// 刷新图书列表
			renderBookList(creator);
			bookModifyModal.hide();
		}).catch(error =>{
			 // console.log(error);
			 alert(error.response.data.message);
		})
});


