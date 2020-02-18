<template>
    <div>
        <article class="card mb-5 mt-3">
            <div class="card-body" v-if="article && author">
                <h2 class="mb-0">{{ article.title }}</h2>
                <span class="text-muted small mt-0 mb-0">Автор: {{ author.username }}, {{ getPublishDate }}</span>
                <hr class="mt-0">
                <div v-html="article.body" class="article-body m-3" style="white-space: pre-line;"></div>
<!--                <p>{{article.body}}</p>-->
                <hr class="mt-0 mb-0">
                <span class="text-muted small mt-0 mb-0">Статус: {{ article.status }}</span>

            </div>
        </article>
        <form method="post" class="card form-create mb-5 mt-3" @submit.prevent="create">
            <div class="card-body">
                <div class="form-group text-left">
                    <textarea v-model="comment_body" class="form-control" placeholder="Комментарий" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Комментарий'" rows="3" minlength="5" />
                </div>

                <div class="row d-flex flex-fill justify-content-between align-items-center mt-4">
                    <div class="col-md-6">
                            <button type="submit" class="btn btn-primary btn-block btn-md">Оставить комментарий</button>
                    </div>

                </div>
            </div>
        </form>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "FullArticle",
        data() {
            return {
                article: null,
                author: null,
                loading: false,
                comment_body: '',
            }
        },
        computed: {
            getPublishDate: function () {
                return new Date(this.article.publish).toLocaleString("ru", {hour: 'numeric', minute: 'numeric', day: 'numeric', month: 'long', year: 'numeric'})

            },
        },
        methods: {
            getPublishDate: function () {
                return new Date(this.$props.article.publish).toLocaleString("ru", {hour: 'numeric', minute: 'numeric', day: 'numeric', month: 'long', year: 'numeric'})

            }
        },
        beforeCreate() {
            this.loading = true //the loading begin
            axios
            .get('https://atarasov.ru/api/posts/' + this.$route.params.id + '/?access_token=mycSH1GDCTr2daqnxeEdWvde1X5QQ1')
            .then(response => {
                this.loading = false
                this.article = response.data

                axios
                .get('https://atarasov.ru/api/users/' + this.article.author + '/?access_token=mycSH1GDCTr2daqnxeEdWvde1X5QQ1')
                .then(response => {
                    this.author = response.data
                })
                .catch(error => {
                    this.loading = false
                    this.$router.push('/blog')
                })

            })
            .catch(error => {
                this.loading = false
                this.$router.push('/blog')
            })
        }
    }
</script>

<style scoped>
.card {
    border: 0;
    box-shadow: 0 0 22px 1px rgba(179,177,179,0.19);

}

.article-body >>> h2 {
    color: green;
}

input::placeholder, textarea::placeholder {
    color: #c9c9c9;
}

.form-control:focus {
    box-shadow: none !important;
}
</style>