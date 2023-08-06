
Vue.component('editables-list', {
    mixins: [
        itemListMixin
    ],
    data: function() {
        return {
            url: this.$urls.pages.api_content,
            params: {
                o: '-created_at'
            }
        }
    },

    mounted: function(){
        this.get()
    }
});


Vue.component('editables-detail', {
    mixins: [
        itemMixin
    ],
    data: function() {
        return {
            url: this.$urls.pages.api_content,
            comments: {count: 0, results: []},
            message: ""
        }
    },
    methods: {
        submitFollow: function() {
            var vm = this;
            vm.reqPost(vm.isFollowing ? this.$urls.pages.api_unfollow
                       : this.$urls.pages.api_follow,
                function success(resp) {
                    vm.isFollowing = !vm.isFollowing;
                    vm.nbFollowers += vm.isFollowing ? 1 : -1;
            });
            return false;
        },
        submitVote: function() {
            var vm = this;
            vm.reqPost(vm.isUpVote ? this.$urls.pages.api_downvote
                       : this.$urls.pages.api_upvote,
                function success(resp) {
                    vm.isUpVote = !vm.isUpVote;
                    vm.nbUpVotes += vm.isUpVote ? 1 : -1;
            });
            return false;
        },
        submitComment: function() {
            var vm = this;
            vm.reqPost(this.$urls.pages.api_comments, {
                text: vm.message},
            function success(resp) {
                vm.message = "";
                vm.comments.results.push(resp);
                vm.comments.count += 1;
            });
            return 0;
        },
    },
    mounted: function() {
        var vm = this;
        vm.get()
        vm.reqGet(this.$urls.pages.api_comments,
        function success(resp) {
            vm.comments = resp;
        });
    }
});
