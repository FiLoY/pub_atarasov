<template>
    <div class="blog mt-3">
        <div v-if="loading">
            <div class="text-center">
                <div class="spinner-grow" style="width: 3rem; height: 3rem;" role="status">
                    <span class="sr-only">Загрузка...</span>
                </div>
            </div>
        </div>
        <div class="text-right">
            <router-link :to="{ name: 'create_article'}" class="btn btn-primary mb-3"><span style="font-size: 1.5em;">+</span><span> Написать статью</span></router-link>
        </div>
        <div v-if="error_message" class="text-center mt-5">
            <h4>{{ error_message }}</h4>
        </div>
        <post v-for="article in articles" v-bind:article="article"/>
    </div>
</template>

<script>
    import post from "../components/post";
    import axios from 'axios'
    export default {
        name: "Blog",
        components: {
            post
        },
        data() {
            return {
                articles: null,
                loading: false,
                error_message: '',

            }
        },

        created() {
            this.loading = true //the loading begin
            axios
            .get('https://atarasov.ru/api/posts/?access_token=YOURTOKEN')
            .then(response => {
                this.loading = false
                this.articles = response.data

            })
            .catch(error => {
                this.loading = false
                this.error_message = 'Упс...Что-то не загрузилось...Обновите страницу'

            })
        }
    }
</script>

<style scoped>
.spinner-grow {
    color: #854ed2 !important;

}

</style>