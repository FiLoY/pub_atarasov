<template>
    <div>
        <form class="card form-signin mt-0 mt-md-5" @submit.prevent="login">
            <div class="card-body">
                <h4 class="card-title text-center mb-4 mt-1">Вход</h4>
                <hr>
                <div class="alert alert-danger" role="alert" v-if="errors">
                    {{ errors }}
                </div>
                <div class="form-group">
                    <input v-model="username" type="text" class="form-control" :class="{'is-invalid': errors}" placeholder="Почта" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Почта'">
                </div>
                <div class="form-group">
                    <input v-model.lazy.trim="password" type="password" class="form-control" :class="{'is-invalid': errors}" placeholder="Пароль" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Пароль'">
                </div>

                <div class="row d-flex flex-fill justify-content-md-between justify-content-sm-center align-items-center">
                    <div class="col-md-6 col-sm-12">
                            <button type="submit" class="btn btn-primary btn-block">Войти</button>
                    </div>
                    <div class="col-md-6 col-sm-12 text-md-left text-center mt-3 mt-md-0">
                        <a class="small alink" href="#">Забыли пароль?</a>
                        <div class="w-100 mt-3 mt-md-0"></div>
                        <router-link to="/signup" class="small alink">Зарегистрироваться</router-link>
                    </div>
                </div>
            </div>
        </form>
    </div>
</template>

<script>
    export default {
        name: "Login",
        data() {
            return {
                username: '',
                password: '',
                errors: ''

            };

        },
        computed: {
            isLoggedIn() { return this.$store.getters.isLoggedIn }

        },
        methods: {
            login: function () {
                const {username, password} = this
                if (username && password) {
                    this.$store.dispatch('login', {username, password})
                        .then(() => this.$router.push('/'))
                        .catch(err => {
                            this.errors = 'Пользователь не существует или введены некорректные данные'
                        })
                }
                else {
                    this.errors = 'Введите все данные'
                }
            },
        },
        created() {
            if (this.isLoggedIn) {
                this.$router.push('/')
            }

        }
    }
</script>

<style scoped>
.form-signin {
    width: 100%;
    max-width: 330px;
    margin: 0 auto;
}
input::placeholder {
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
.alink {
    color: #854ed2;
}
</style>