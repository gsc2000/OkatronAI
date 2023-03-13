console.log("program")

const unit1 = document.querySelector('#unit1');
  const input1 = document.querySelector('#input1');
  const unit2 = document.querySelector('#unit2');
  const input2 = document.querySelector('#input2');
  const unit3 = document.querySelector('#unit3');
  const input3 = document.querySelector('#input3');
  const unit4 = document.querySelector('#unit4');
  const input4 = document.querySelector('#input4');
  const unit5 = document.querySelector('#unit5');
  const input5 = document.querySelector('#input5');
  const startButton = document.getElementById('start-button');

  // ドロップダウンの値が変更されたときに実行する関数
  function dropdownChanged(target, input) {
    if (target.value === '2' || target.value === '4' || target.value === '9') {
      input.value = ""
      input.disabled = true;
    } else {
      input.disabled = false;
    }
  }

  // STARTボタンがクリックされたときに実行する関数
  function start() {
    // ドロップダウンと数字入力ボックスの値を取得する
    const value1 = unit1.value === '1' ? input1.value : '';
    const value2 = unit2.value === '1' ? input2.value : '';
    const value3 = unit3.value === '1' ? input3.value : '';
    const value4 = unit4.value === '1' ? input4.value : '';
    const value5 = unit5.value === '1' ? input5.value : '';

    // FastAPIに情報を渡す
    fetch('/mode/3/info', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
        unit1: String(unit1.value),
        value1: String(value1),
        unit2: String(unit2.value),
        value2: String(value2),
        unit3: String(unit3.value),
        value3: String(value3),
        unit4: String(unit4.value),
        value4: String(value4),
        unit5: String(unit5.value),
        value5: String(value5),
      }),
    })
      .then(response => response.json())
      .then(data => {
        console.log(data);
      })
      .catch(error => {
        console.error(error);
      });
  }


  startButton.addEventListener('click', start);

  unit1.addEventListener('change', function(){dropdownChanged(unit1, input1)})
  unit2.addEventListener('change', function(){dropdownChanged(unit2, input2)})
  unit3.addEventListener('change', function(){dropdownChanged(unit3, input3)})
  unit4.addEventListener('change', function(){dropdownChanged(unit4, input4)})
  unit5.addEventListener('change', function(){dropdownChanged(unit5, input5)})
