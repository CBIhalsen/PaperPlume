<template>
  <div style="background-color: #fef9f3;padding: 4.5rem 5rem;display: flex; justify-content: center;flex-direction: column; align-items: center;padding-bottom: 5rem;">
  <div class="show-footer" style="display: flex; padding: 4.5rem 4rem;flex-wrap: wrap;  ">
    <div class="column1 column">
      <h2 data-lang-key="fh2" >General FAQs about our AI Paper Creator</h2>
      <p data-lang-key="fp" style="margin-top: 1rem;">Everything you need to know about PaperPlume and our one-click academic paper generator. Can’t find an answer?  You can talk to Vee, our customer service.</p>
    </div>
    <div class="column2 column">
      <div class="unfold">
        <button data-lang-key="fb1" class="none-button" @click="toggle1">What is PaperPlume?</button>
        <span data-lang-key="fs1" id="content1" v-show="contentn1" >PaperPlume是一款先进的人工智能驱动的学术论文生成器。其操作简单，支持中文，英文，日语等输出语言，它能够快速的生成一篇高质量的论文。
       <br> PaperPlume是为了帮助那些声音、思考和想法需要被充分表达的人。无论你是学生还是教授，论文是你工作的一部分还是你的个人兴趣，PaperPlume都能帮助你以最低的成本和最高的效率，实现你想要的。
        </span>


      </div>
      <div class="unfold">
        <button data-lang-key="fb2" class="none-button" @click="toggle2">How do I use PaperPlume?</button>
        <span data-lang-key="fs2" id="content2" v-show="contentn2" >使用PaperPlume非常简单。您只需在输入框中输入论文标题，点击“提交”按钮即可获得完整的论文大纲。大纲可以自由编辑，通过空格数表示论文的层次结构。在修改大纲时，请确保每个段落标题前的空格数正确无误。如果您有特定的需求，可以在设置中进行详细选择。</span>
        <!-- Add more buttons and content divs as needed -->
      </div>
            <div class="unfold">
        <button data-lang-key="fb3" class="none-button" @click="toggle3">Does PaperPlume only generate academic papers?</button>
        <span data-lang-key="fs3" v-show="contentn3" >PaperPlume是一款多功能的智能写作工具，主要提供学术论文生成服务。除了学术论文，它还能够生成其他类型的文章，如报告、文章和研究摘要。虽然在生成效果方面，学术论文仍然是其最擅长的领域，但你也可以利用PaperPlume来修改PPT。只需提交一个空的PPT模板，并指定所需的主题和风格，你将获得一个符合你预期的PPT演示文稿。无论是学术写作还是PPT制作，PaperPlume都能够满足你的需求。</span>
        <!-- Add more buttons and content divs as needed -->
      </div>
            <div class="unfold">
        <button data-lang-key="fb4" class="none-button" @click="toggle4">Why choose PaperPlume over other paper generators?</button>
        <span data-lang-key="fs4" v-show="contentn4" >PaperPlume是一款采用最先进人工智能技术的论文生成工具，为用户提供领先行业的服务。使用PaperPlume，您可以以约0.5美元的成本，在短短10分钟内生成一篇高质量的论文。我们提供简洁易用的界面，为用户带来极佳的使用体验。相比其他论文生成器，PaperPlume更加灵活高效，让您轻松完成论文写作任务。</span>
        <!-- Add more buttons and content divs as needed -->
      </div>
            <div class="unfold">
        <button data-lang-key="fb5" class="none-button" @click="toggle5">Can a paper created by PaperPlume be checked by the detector to be ai generated?</button>
        <span data-lang-key="fs5" v-show="contentn5" >PaperPlume生成的论文在质量和风格上与人类撰写的论文几乎无法区分。在众多的AI生成器中，PaperPlume生成的论文具有更高的自然性，无法检测出来。然而，如果您发现您的论文被AI生成，我们将提供全额退款。为了确保您获得一篇完美的论文，我们建议您使用PaperPlume生成的论文作为草稿，并在此基础上添加您自己的观点和分析，以使其更符合您个人的风格和要求。</span>
        <!-- Add more buttons and content divs as needed -->
      </div>
    </div>
  </div>
    <div class="contact-us" style="display: flex;flex-wrap: wrap;">
      <p style="margin-right: 1rem;">Copyrights &copy; 2023 Verseeding   </p>
<a data-lang-key="ca1" href="mailto:kulleeter@gmail.com">Contact Us  |</a> <a data-lang-key="ca2" >Support  |</a>  <a data-lang-key="ca3"  href="Blog" target="_blank" >Blog  |</a>  <a data-lang-key="ca5"  href="TermsServiceandPrivacyPolicy.html" target="_blank">Cookie Policy   |</a> <a data-lang-key="ca6"  href="TermsServiceandPrivacyPolicy.html" target="_blank" >Privacy Policy   |</a>  <a>Powered by | </a> <a >Verseeding</a>
<!--            <p>Copyrights &copy; 2023 Verseeding | Designed by <a href="https://github.com/CBIhalsen" target="_blank">Felix Chen</a>-->
<!--            Email: <a href="mailto:kulleeter@gmail.com">kulleeter@gmail.com</a>-->
<!--            </p>-->
<!--      <p></p>-->
        </div>
    </div>
</template>

<script>
export default {
   data() {
    return {
      contentn1: false,
      contentn2: false,
      contentn3: false,
       contentn4: false,
      contentn5: false,
    };
  },
  methods: {
    toggle1() {
      this.contentn1 = !this.contentn1;
    },
        toggle2() {
      this.contentn2 = !this.contentn2;
    },
        toggle3() {
      this.contentn3 = !this.contentn3;
    },
        toggle4() {
      this.contentn4 = !this.contentn4;
    },
        toggle5() {
      this.contentn5 = !this.contentn5;
    },

  },
};
</script>
<style>
   .contact-us{
     display: flex;
     margin-top: 1.5rem;
   }
         .contact-us p {
            margin: 0;
           font-size: 1rem;
            line-height: 1.5;
            /*color: #00ff00; !* 修改文本颜色为蓝色 *!*/
        }

       .contact-us a {
         margin-right: 0.5rem;
           font-size: 1rem;
            color: #000000;
            text-decoration: none;
        }

       .contact-us a:hover {
            text-decoration: underline;
        }



.column h2 {
  font-size: 1.5rem;
  color: #333;
}

.column  p {
  font-size: 0.9rem;
  color: #666;
}

.column  span {
    font-size: 0.9rem;
  color: #666;
  text-decoration: none;
}


.show-footer {
   height: 80%;
    background-color: white;
    padding: 20px;
    width: 100%;
    display: flex;
  background-clip: padding-box;
    justify-content: space-between;
}
.column1 {
  margin-top: 1rem;
  margin-bottom: 1rem;
  margin-left: 2.2rem;
    width: 270px;
  max-width: 100vw;
}
.column2 {
  margin-left: 2.2rem;
    width: 756px;
    max-width: 100vw;
}
.none-button {
  margin-bottom: 0.6rem;
    text-align: left;
  color: #333;
  border: none;
  padding: 0px;
  background: transparent;
  box-shadow: none;
  width: 100%;
}
.none-button:hover,
.none-button:focus {
  background-color: transparent;
  border: none;
   outline: none;
  /* 添加你想要的样式变化 */
}

/*.content {*/
/*  color: black;*/
/*    display: flex;*/
/*    padding: 0px;*/

/*}*/
.unfold{
  margin-bottom: 1.2rem;
  border-bottom: 1px solid #090d7d;
  padding-bottom: 0.9rem;
}
</style>