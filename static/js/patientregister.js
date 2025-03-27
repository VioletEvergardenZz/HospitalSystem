window.onload = function () {
	var errorMessage = document.querySelector('.error-message');
	if (errorMessage) {
		setTimeout(function () {
			errorMessage.style.display = 'none';
		}, 3000);
	}
};

function validateForm() {
	var phone = document.forms["register_form"]["phone"].value;
	var password = document.forms["register_form"]["password"].value;
	var confirm_password = document.forms["register_form"]["confirm_password"].value;
	var name = document.forms["register_form"]["name"].value;
	var sex = document.forms["register_form"]["sex"].value;
	var age = document.forms["register_form"]["age"].value;

	// 检查所有字段是否为空
	if (!phone || !password || !confirm_password || !name || !sex || !age) {
		alert("请填写所有字段");
		return false;
	}

	var phoneRegex = /^1[3-9]\d{9}$/;
	if (!phoneRegex.test(phone)) {
		alert("请输入有效的手机号码");
		return false;
	}

	if (password.length < 6) {
		alert("密码长度不能少于6位");
		return false;
	}

	if (password !== confirm_password) {
		alert("两次输入的密码不一致，请重新输入");
		return false;
	}

	var nameRegex = /^[a-zA-Z\u4e00-\u9fa5]+$/;
	if (!nameRegex.test(name)) {
		alert("患者姓名只能包含英文和中文");
		return false;
	}

	if (sex === "") {
		alert("请选择患者性别");
		return false;
	}

	var ageRegex = /^\d{1,3}$/;
	if (!ageRegex.test(age)) {
		alert("请输入有效的年龄");
		return false;
	}

	return true;
}