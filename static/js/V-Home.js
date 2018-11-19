var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#wrapper-app',
    data: {
        activeSection: 0,
        img: ''
    },
    methods:{
        imgPreviewChange: function(e){
            let input = e.target;
            let reader = new FileReader();

            reader.onload = function (e) {
                let imgPrev = document.getElementById('image-preview');
                imgPrev.setAttribute('src', e.target.result);
                this.img = e.target.result;
            }

            reader.readAsDataURL(input.files[0]);
        }
    }
});
