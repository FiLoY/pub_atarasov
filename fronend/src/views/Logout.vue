<template>
    <div>
        Выходим, господа!
    </div>
</template>

<script>
    export default {
        name: "Logout",
        methods: {
            logout: function () {
                this.$store.dispatch('logout')
                .then(() => {
                    this.$router.push('/login')
                })
            }
        },
        mounted() {
            this.logout()
        }
    }
</script>

<style scoped>

</style>