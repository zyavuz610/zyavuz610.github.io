let score = 0;
const correctSound = new Audio("sounds/correct.mp3");
const wrongSound = new Audio("sounds/wrong.mp3");

// Tıklanabilir (gaze ile seçilebilir) nesnelere olay ekle
AFRAME.registerComponent("gaze-listener", {
  init: function () {
    this.el.addEventListener("click", () => {
      checkAnswer(this.el.id);
    });
  },
});

function checkAnswer(selectedId) {
  const word = document.getElementById("word").getAttribute("text").value;
  let correct = false;

  // Basit örnek veri: doğru cevaplar
  const answers = {
    dog: "rightOption",
    apple: "leftOption",
    car: "rightOption",
  };

  if (answers[word] === selectedId) {
    correct = true;
  }

  if (correct) {
    correctSound.play();
    score += 10;
    document.getElementById("score").setAttribute("text", "value", `Score: ${score}`);
  } else {
    wrongSound.play();
  }

  // Yeni kelimeye geç (örnek basit liste)
  nextWord();
}

function nextWord() {
  const words = ["dog", "apple", "car"];
  const meanings = {
    dog: ["cat", "köpek"],
    apple: ["armut", "elma"],
    car: ["uçak", "araba"],
  };

  const randomIndex = Math.floor(Math.random() * words.length);
  const word = words[randomIndex];
  const [left, right] = meanings[word];

  // Güncelle kelime ve seçenekler
  document.getElementById("word").setAttribute("text", "value", word);
  document.querySelectorAll("a-entity[text]").forEach((entity) => {
    const pos = entity.getAttribute("position");
    if (pos.x < 0) entity.setAttribute("text", "value", left);
    else if (pos.x > 0) entity.setAttribute("text", "value", right);
  });
}
