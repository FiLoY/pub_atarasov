<template>
    <article class="card mb-5">
<!--        <div class="card-header">-->
<!--            {{ article.title }}-->
<!--        </div>-->
        <div class="card-body">
            <router-link  v-bind:to="'blog/' + article.id" class="text-muted"><h3>{{ article.title }}</h3></router-link>
            <p>{{ article.body.slice(0, 500) }}</p>
            {{ getPublishDate() }}
        </div>

    </article>
</template>

<script>
    export default {
        name: "post",
        props: ['article'],
        data() {
            return {
                publish_date: 1
            }
        },
        methods: {
            getPublishDate: function () {
                return new Date(this.$props.article.publish).toLocaleString("ru", {hour: 'numeric', minute: 'numeric', day: 'numeric', month: 'long', year: 'numeric'})

            }
        }
    }
</script>

<style scoped>
.card {
    border: 0;
    box-shadow: 0 0 22px 1px rgba(179,177,179,0.19);

}
</style>