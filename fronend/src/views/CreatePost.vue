<template>
    <div>
        <form method="post" class="card form-create mt-0 mt-md-5" @submit.prevent="create">
            <div class="card-body">
                <h4 class="card-title text-center mb-4 mt-1">Создание статьи</h4>
                <hr>
                <div class="alert alert-danger" role="alert" v-if="errors.length">
                    <div v-for="error in errors">{{ error }}</div>

                </div>
                <div class="form-group text-left">
                    <input v-model="title" type="text" class="form-control" :class="{'is-invalid': title_error.length}" placeholder="Приятный заголовок" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Приятный заголовок'">
                    <small class="form-text ml-1 mr-1 text-danger" v-if="title_error.length" v-for="err in title_error">
                        {{ err }}
                    </small>
                    <small class="form-text ml-1 mr-1 text-muted" v-if="!title_error.length">
                        Заголовок должен быть приятным!
                    </small>
                </div>
                <div class="form-group text-left">
                    <textarea v-model="body" class="form-control" :class="{'is-invalid': body_error.length}" placeholder="Текст" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Текст'" rows="5" minlength="5" />
                    <small class="form-text ml-1 mr-1 text-danger" v-if="body_error.length" v-for="err in body_error">
                        {{ err }}
                    </small>
                    <small class="form-text ml-1 mr-1 text-muted" v-if="!body_error.length">
                        Текст статьи, пока просто текст.
                    </small>
                </div>

                <div class="row d-flex flex-fill justify-content-between align-items-center mt-4">
                    <div class="col-md-6">
                            <button type="submit" class="btn btn-primary btn-block btn-md">Опубликовать</button>
                    </div>

                </div>
            </div>
        </form>
    </div>
</template>

<script>
    export default {
        name: "CreatePost",
        data() {
            return {
                title: '',
                body: '',
                errors: [],
                title_error: [],
                body_error: [],
                password_error: [],
            };

        },
        methods: {
            create: function () {
                this.errors = []
                const { title, body } = this

                this.$store.dispatch('createPost', {title, body})
                    .then(() => this.$router.push('/blog'))
                    .catch(err => {
                        this.errors.push('Упс')
                    })
            }
        },
    }
</script>

<style scoped>
.form-create {
    width: 100%;
    /*max-width: 800px;*/
    margin: 0 auto;
}
input::placeholder, textarea::placeholder {
    color: #c9c9c9;
}
.form-control {
/*border-top: 0;*/
}
.form-control:focus {
    box-shadow: none !important;
}

.card {
    border: 0;
    box-shadow: 0 0 22px 1px rgba(179,177,179,0.19);
}

</style>