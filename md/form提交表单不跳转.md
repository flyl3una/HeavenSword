## HTML中form表单提交内容不跳转页面

1.正常的form点击提交按钮后页面会跳转

```html
<form method="post">
  <input type="text" name="in">
  <input type="submit" value="提交">
</form>
```

2.可以采用锚点的方法，在页面中添加一个iframe框架，设置为不显示，然后将form的target属性设为iframe的name，得到的数据会到达iframe框架中。而iframe不显示。为了显示到原本的页面上，可以使用js将iframe设置为显示或者直接将iframe的得到的数据传到父页面上。

```html
<html>
  <iframe name="target_form"></iframe>
  <form method="post" target="target_form">
    <input type="text" name="in">
    <input type="submit" value="提交">
  </form>
  <div class="show_result">
  </div>
</html>

<script>
	var show_result = function(ret){
      $(".show_result").html(ret);
	}
</script>
```

通过上面的代码可以将form提交后得到的返回数据显示在show_result的div中。