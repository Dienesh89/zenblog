// views formatter

const formatView = (num)=>{
    let formattedNum;

    if (num < 1000) {
        formattedNum = num.toString();
    } else if (num < 1000000) {
        formattedNum = (num / 1000).toFixed(1) + "K";
    } else {
        formattedNum = (num / 1000000).toFixed(1) + "M";
    }

    document.getElementById("view").innerHTML = `(${formattedNum} views)`
}
