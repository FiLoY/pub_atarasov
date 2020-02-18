<template>
    <div id="VueStudy" class="vue-study m-3">
        <div class="card card-body mb-3">
            <p>{{ message }}</p>
        <input v-model="message" v-once>
  <button v-on:click="reverseMessage">Перевернуть сообщение</button>

        </div>


        <div class="card card-body mb-3">
            <button v-on:click="show = !show">
    Переключить
  </button>
  <transition name="fade">
    <p v-if="show">привет</p>
  </transition>
        </div>



    </div>
</template>

<script>
    export default {
        name: "VueStudy",
        data() {
            return {
                message: 'Переверни меня, пользователь!',
                show: true

            }
        },
        methods: {
            reverseMessage: function () {
                this.message = this.message.split('').reverse().join('')
            }
        }
    }
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active до версии 2.1.8 */ {
  opacity: 0;
}
</style>