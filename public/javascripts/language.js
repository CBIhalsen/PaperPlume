
let languagePack;

  window.onload = function() {

        var userLanguage = navigator.language || navigator.userLanguage;
if (userLanguage !== 'zh-CN' && userLanguage !== 'zh-TW' && userLanguage !== 'ja') {
  userLanguage = 'en';
}

        // 输出首选语言到控制台
        console.log("浏览器首选语言：" + userLanguage);
languageSwitcherHandler(event,userLanguage);

adjustLanguageSwitcher();


      let button = document.getElementById('language-button');
      let switcher = document.getElementById('language-switcher');
      button.addEventListener('mouseover', function() {
    switcher.style.display = 'block';




});
switcher.addEventListener('mouseover', function() {
    switcher.style.display = 'block';
});
button.addEventListener('mouseout', function() {
    switcher.style.display = 'none'; // 恢复原来的 display 属性
});
switcher.addEventListener('mouseout', function() {
    switcher.style.display = 'none'; // 恢复原来的 display 属性
});

    switcher.addEventListener('click', languageSwitcherHandler);
    function languageSwitcherHandler(e,language) {

    if (!language){
      language = e.target.getAttribute('data-lang');
    }

    const folder = './javascripts/';
    const filename = '.json';
    const path = folder + language+ filename;
    console.log(path)



 fetch(path)
  .then(response => response.json())
  .then(data => {
    languagePack =data
    console.log(languagePack)


    console.log(language);
    let elements = document.querySelectorAll('[data-lang-key]');
    elements.forEach(function(element) {
    if (element.hasAttribute('data-lang-key')) {
      let key = element.getAttribute('data-lang-key');
      element.innerHTML = languagePack[language][key];
    }
    });
    function decreaseFontSize(className, percentage) {
    var elements = document.getElementsByClassName(className);
    for (var i = 0; i < elements.length; i++) {
        var element = elements[i];
        var currentFontSize = parseFloat(window.getComputedStyle(document.documentElement).fontSize);
        var newFontSize = currentFontSize * (1 - percentage);
        console.log(newFontSize)

        element.style.fontSize = newFontSize + 'px';
    }
}
let percent=0;
if (language=='en' ){
    percent=0.1;
     decreaseFontSize('faa', percent);

     decreaseFontSize('modal-body', percent);
    document.getElementById('signup-button').style.fontSize = '1rem';
} else if(language=='ja'){
     percent=0.11;
      decreaseFontSize('modal-body', 0.1);
     decreaseFontSize('faa', percent-0.11);
    decreaseFontSize('signup-btn', percent+0.2);
}
else {
    percent=0
     decreaseFontSize('modal-body', 0);
    document.getElementById('signup-button').style.fontSize = '1rem';
}
// 使用示例
decreaseFontSize('writing1', percent);

    let links = document.querySelectorAll('.language-a');
    links.forEach(function(link) {
        if (link.getAttribute('data-lang') === language) {
            link.style.color = "blue";
        } else {
            link.style.color = "black";
        }
    });
      console.log(languagePack.en);
    // 在这里使用 languagePack 变量进行其他操作
  })
  .catch(error => {
    console.error('Error:', error);
  });

    // 获取select元素
let selectElement = document.getElementById("language-select");

// 设置要选择的值
let selectedValue = userLanguage;

// 遍历select的选项，找到与selectedValue匹配的选项
for (var i = 0; i < selectElement.options.length; i++) {
  if (selectElement.options[i].value === selectedValue) {
    // 设置选中状态
    selectElement.options[i].selected = true;
    console.log('选中');
       console.log(selectElement.options[i]);
    break;
  }
}

let styleselectElement = document.getElementById("writing-style-select");

// 设置要选择的值
let styleselectedValue ;
if (userLanguage=='zh-CN'){
    styleselectedValue='《中国社会科学》'
} else if(userLanguage=='zh-TW'){
     styleselectedValue='《中央研究院歷史語言研究所集刊》'
} else if(userLanguage=='ja'){
     styleselectedValue='《日本教育社会学会雑誌》'
} else {
    styleselectedValue='Nature'
}

// 遍历select的选项，找到与selectedValue匹配的选项
for (var i = 0; i < styleselectElement.options.length; i++) {
  if (styleselectElement.options[i].value === styleselectedValue) {
    // 设置选中状态
    styleselectElement.options[i].selected = true;
    break;
  }
}




}


      // switcher.addEventListener('click', function(e) {
      //     e.preventDefault();
      //     language = e.target.getAttribute('data-lang');
      //     console.log(language);
      //
      //     let elements = document.querySelectorAll('[data-lang-key]');
      //     elements.forEach(function(element) {
      //         let key = element.getAttribute('data-lang-key');
      //         element.textContent = languagePack[language][key];
      //     });
      //
      //     let links = document.querySelectorAll('.language-a');
      //     links.forEach(function(link) {
      //         if (link.getAttribute('data-lang') === language) {
      //             link.style.color="blue";
      //         } else {
      //           link.style.color="black";
      //         }
      //     });
      // });
  }


function adjustLanguageSwitcher() {
  var button = document.getElementById('language-button');
  var switcher = document.getElementById('language-switcher');

  // 获取元素的位置信息
  var buttonRect = button.getBoundingClientRect();

  // 设置语言切换器的位置
  // switcher.style.position = 'absolute';
  // switcher.style.top = (buttonRect.top + buttonRect.height) + 'px';
  switcher.style.right = (document.documentElement.clientWidth - buttonRect.right) + 'px';
}