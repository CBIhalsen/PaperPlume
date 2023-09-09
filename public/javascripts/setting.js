
         var settingsPopup = document.getElementById("settings-popup");
        var languageSelect = null;
        var writingStyleSelect = null;
        var textarea = null;
        var model = null;
        function saveSettings() {
          localStorage.setItem("language", languageSelect.value);
          localStorage.setItem("writingStyle", writingStyleSelect.value);
          localStorage.setItem("textareaValue", textarea.value);
          localStorage.setItem("modelValue", model.value);
        }



        function loadSettings() {
          const savedLanguage = localStorage.getItem("language");
          const savedWritingStyle = localStorage.getItem("writingStyle");
          const savedTextareaValue = localStorage.getItem("textareaValue");
          const savedModelValue = localStorage.getItem("modelValue");
          if (savedLanguage) {
            languageSelect.value = savedLanguage;
            // alert(savedLanguage)
          }
          if (savedWritingStyle) {
            writingStyleSelect.value = savedWritingStyle;
            // alert(savedWritingStyle)
          }
          if (savedTextareaValue) {
            textarea.value = savedTextareaValue;
            // alert(savedTextareaValue)
          }
          if (savedModelValue) {
            model.value = savedModelValue;
            // alert(savedTextareaValue)
          }
        }

        function openSettingsPopup() {
          settingsPopup.style.display = "block";
          loadSettings();
        }

        function closeSettingsPopup() {
          saveSettings();
          settingsPopup.style.display = "none";
        }

        document.getElementById("settings-btn").addEventListener("click", openSettingsPopup);

        document.querySelector(".close-btn").addEventListener("click", closeSettingsPopup);

        textarea = document.getElementById("textarea");
        textarea.addEventListener("input", function() {
          var charCounter = document.getElementById("char-counter");
          charCounter.textContent =  this.value.length ;
        });

        // 初始化
        languageSelect = document.getElementById("language-select");
        writingStyleSelect = document.getElementById("writing-style-select");
        textarea = document.getElementById("textarea");
        model = document.getElementById("model-select");