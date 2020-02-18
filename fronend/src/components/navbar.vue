<template>
<header class="navbar sticky-top navbar-expand-lg navbar-light bg-light shadow-sm">
    <router-link to="/" class="navbar-brand">{{ brand }}</router-link>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"/>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <router-link to="/blog" class="nav-item nav-link" >Статьи</router-link>
                    <router-link to="/vue-study" class="nav-item nav-link" >Учим Vue</router-link>
                </div>
            </div>
            <div class="right">
                <router-link to="/login" class="text-muted" v-if="!isLoggedIn">Войти</router-link>
                <router-link to="/logout" class="text-muted" v-if="isLoggedIn">Выйти</router-link>
            </div>
        </header>
</template>

<script>
    export default {
        name: "navbar",
        data() {
            return {
                brand: 'A. TARASOV',
            }
        },
        computed: {
            isLoggedIn() { return this.$store.getters.isLoggedIn },
        },
        methods: {

        }
    }
</script>

<style scoped>
/*.navbar-dark {*/
/*  background-color: red;*/
/*}*/
</style>
