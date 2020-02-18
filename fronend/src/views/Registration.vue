<template>
    <div>
        <form method="post" class="card form-signup mt-0 mt-md-5" @submit.prevent="register">
            <div class="card-body">
                <h4 class="card-title text-center mb-4 mt-1">Регистрация</h4>
                <hr>
                <div class="alert alert-danger" role="alert" v-if="errors.length">
                    <div v-for="error in errors">{{ error }}</div>

                </div>
                <div class="form-group text-left">
                    <input v-model="username" ref="username" type="text" class="form-control" :class="{'is-invalid': username_error.length}" placeholder="Имя пользователя" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Имя пользователя'">
                    <small class="form-text ml-1 mr-1 text-danger" v-if="username_error.length" v-for="err in username_error">
                        {{ err }}
                    </small>
                    <small class="form-text ml-1 mr-1 text-muted" v-if="!username_error.length">
                        Имя пользователя может содержать только латинские буквы и цифры и должно содержать 4-20 символа
                    </small>
                </div>
                <div class="form-group text-left">
                    <input v-model="email" ref="email" type="text" class="form-control" :class="{'is-invalid': email_error.length}" placeholder="Почта" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Почта'">
                    <small class="form-text ml-1 mr-1 text-danger" v-if="email_error.length" v-for="err in email_error">
                        {{ err }}
                    </small>
                    <small class="form-text ml-1 mr-1 text-muted" v-if="!email_error.length">
                        Почта может содержать только латинские буквы и цифры и должна содержать минимум 4 символа.
                    </small>
                </div>
                <div class="form-group text-left">
                    <input v-model="password" ref="password" type="password" class="form-control" :class="{'is-invalid': password_error.length}" placeholder="Пароль" onfocus="this.placeholder = ''" onblur="this.placeholder = 'Пароль'">
                    <small class="form-text ml-1 mr-1 text-danger" v-if="password_error.length" v-for="err in password_error">
                        {{ err }}
                    </small>
                    <small class="form-text ml-1 mr-1 text-muted" v-if="!password_error.length">
                        Пароль может содержать только латинские буквы и цифры и должен содержать 8-20 символов
                    </small>
                </div>
                <div class="row d-flex flex-fill justify-content-between align-items-center mt-4">
                    <div class="col-md-8">
                            <button type="submit" class="btn btn-primary btn-block btn-sm small">Зарегестрироваться</button>
                    </div>

                </div>
            </div>
        </form>
    </div>
</template>

<script>
    export default {
        name: "Registration",
        data() {
            return {
                username: '',
                email: '',
                password: '',
                errors: [],
                username_error: [],
                email_error: [],
                password_error: [],
            };

        },
        computed: {
            isLoggedIn() { return this.$store.getters.isLoggedIn }

        },
        methods: {
            register: function () {
                this.errors = []
                this.username_error = []
                this.email_error = []
                this.password_error = []
                const { username, email, password } = this

                if (!username) {
                    this.username_error.push('Заполните имя пользователя')
                } else if (username.length < 4 || username.length > 20) {
                    this.username_error.push('Имя пользователя может содержать только латинские буквы и цифры')
                } else if (!this.validText(username)) {
                    this.username_error.push('Поле некорректно заполнено')
                }

                if (!email) {
                    this.email_error.push('Заполните поле почты')
                } else if (email.length < 4) {
                    this.email_error.push('Почта должна содержать минимум 4 символа')
                } else if (!this.validEmail(email)) {
                    this.email_error.push('Почта может содержать только латинские буквы и цифры')
                }

                if (!password) {
                    this.password_error.push('Заполните пароль')
                } else if (password.length < 8 || password.length > 20) {
                    this.password_error.push('Пароль должен содержать 8-20 символов')
                } else if (!this.validText(password)) {
                    this.password_error.push('Пароль может содержать только латинские буквы и цифры')
                }


                if (this.errors.length || this.username_error.length || this.email_error.length || this.password_error.length) {
                    return false
                }

                this.$store.dispatch('register', {username, email, password})
                    .then(() => this.$router.push('/'))
                    .catch(err => {
                        this.errors.push('Пользовотель с данной почтой и/или именем пользователя уже существует. Попробуйте войти или восстановить пароль')
                    })
            },
            validEmail: function (email) {
                var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
                return re.test(email);
            },
            validText: function (text) {
                var re = /^[a-zA-Z0-9]*$/;
                return re.test(text);
            }
        },
        created() {
            if (this.isLoggedIn) {
                this.$router.push('/')
            }

        }
    }
</script>

<style scoped>
.form-signup {
    width: 100%;
    max-width: 400px;
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
</style>