from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import datetime, time

from spy.models import Blogger, Post

class SpyViewsTestCase(TestCase):
    def adduser(self, name, email):
        username = str(name)
        useremail = str(email)
        return User.objects.create_user(username, useremail, username+'password')
    def addblogger(self, user, avatar_number):
        username = user
        avatar_num = int(avatar_number)
        return Blogger.objects.create(
            user=username,
            avatar='default' + str(avatar_num)  + '.png'
        )
    def addpost(self, blogger, title, body):
        blogger = blogger
        title = str(title)
        body = str(body)
        slug = slugify(title)
        return Post.objects.create(
            blogger=blogger,
            title=title,
            body=body,
            slug=slug,
        )
    def test_index_status_without_post(self):
        resp = self.client.get(reverse('spy:index'))
        self.assertEqual(resp.status_code, 200)
    def test_index_status_with_post(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        resp = self.client.get(reverse('spy:index'))
        self.assertEqual(resp.status_code, 200)
    def test_index_content_with_post(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        resp = self.client.get(reverse('spy:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "media/default1.png")
        self.assertContains(resp, "Post #1")
        self.assertContains(resp, "by John")
        self.assertNotContains(resp, "by john")
        self.assertContains(resp, "body text for test")
    def test_index_status_with_posts(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        user_2 = self.adduser('jane', 'doe@thebeatles.com')
        blogger_2 = self.addblogger(user_2, 2)
        post_2 = self.addpost(blogger_2, 'Post #2', 'body text for test2')
        resp = self.client.get(reverse('spy:index'))
        self.assertEqual(resp.status_code, 200)
    def test_index_content_with_posts(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        user_2 = self.adduser('jane', 'doe@thebeatles.com')
        blogger_2 = self.addblogger(user_2, 2)
        post_2 = self.addpost(blogger_2, 'Post #2', 'body text for test2')
        resp = self.client.get(reverse('spy:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "media/default1.png")
        self.assertContains(resp, "Post #1")
        self.assertContains(resp, "by John")
        self.assertNotContains(resp, "by john")
        self.assertContains(resp, "body text for test")
        self.assertContains(resp, "media/default2.png")
        self.assertContains(resp, "Post #2")
        self.assertContains(resp, "by Jane")
        self.assertNotContains(resp, "by jane")
        self.assertContains(resp, "body text for test2")
    def test_index_content_with_post_modified(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        the_post = Post.objects.get(title='Post #1')
        the_post.body = 'modified'
        the_post.save()
        resp = self.client.get(reverse('spy:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "media/default1.png")
        self.assertContains(resp, "Post #1")
        self.assertContains(resp, "by John")
        self.assertNotContains(resp, "by john")
        self.assertNotContains(resp, "body text for test")
        self.assertContains(resp, "modified")
    def test_index_content_with_posts_modified(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test1')
        user_2 = self.adduser('jane', 'doe@thebeatles.com')
        blogger_2 = self.addblogger(user_2, 2)
        post_2 = self.addpost(blogger_2, 'Post #2', 'body text for test2')
        the_post = Post.objects.get(title='Post #1')
        the_post.body = 'modified'
        the_post.save()
        the_post2 = Post.objects.get(title='Post #2')
        the_post2.title = 'Modified #2 Post'
        the_post2.save()
        resp = self.client.get(reverse('spy:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "media/default1.png")
        self.assertContains(resp, "Post #1")
        self.assertContains(resp, "by John")
        self.assertNotContains(resp, "by john")
        self.assertNotContains(resp, "body text for test1")
        self.assertContains(resp, "modified")
        self.assertContains(resp, "media/default2.png")
        self.assertNotContains(resp, "Post #2")
        self.assertContains(resp, "Modified #2 Post")
        self.assertContains(resp, "by Jane")
        self.assertNotContains(resp, "by jane")
        self.assertContains(resp, "body text for test2")
    def test_post_status_with_post(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        resp = self.client.get(reverse('spy:post_detail', args=(1,)))
        self.assertEqual(resp.status_code, 200)
    def test_post_slug_status_with_post(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        resp = self.client.get(reverse('spy:post_slug', args=(slugify(post_1.title),)))
        self.assertEqual(resp.status_code, 200)
    def test_post_slug_status_with_post_modified(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        the_post = Post.objects.get(title='Post #1')
        the_post.title = 'Modified #1 Post'
        the_post.save()
        resp = self.client.get(reverse('spy:post_slug', args=(slugify(post_1.title),)))
        self.assertEqual(resp.status_code, 200)
        resp2 = self.client.get(reverse('spy:post_slug', args=(slugify("Post #1"),)))
        self.assertEqual(resp2.status_code, 200)
        self.assertNotContains(resp2, "Post #1")
        self.assertContains(resp2, "Modified #1 Post")
    def test_post_content_with_post(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        resp = self.client.get(reverse('spy:post_slug', args=(slugify(post_1.title),)))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "media/default1.png")
        self.assertContains(resp, "Post #1")
        self.assertContains(resp, "by John")
        self.assertNotContains(resp, "by john")
        self.assertContains(resp, "body text for test")
    def test_post_content_return_to_index(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        resp = self.client.get(reverse('spy:post_slug', args=(slugify(post_1.title),)))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Return to Index")
        self.assertContains(resp, reverse('spy:post_slug', args=(slugify(post_1.title),)))
        self.assertContains(resp, reverse('spy:index'))
    def test_post_content_with_post_modified(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        the_post = Post.objects.get(title='Post #1')
        the_post.body = 'modified'
        the_post.save()
        resp = self.client.get(reverse('spy:post_slug', args=(slugify(post_1.title),)))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "media/default1.png")
        self.assertContains(resp, "Post #1")
        self.assertContains(resp, "by John")
        self.assertNotContains(resp, "by john")
        self.assertNotContains(resp, "body text for test")
        self.assertContains(resp, "modified")
    def test_archives_status_without_post(self):
        resp = self.client.get(reverse('spy:archives'))
        self.assertEqual(resp.status_code, 200)
    def test_archives_status_with_post(self):
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        resp = self.client.get(reverse('spy:archives'))
        self.assertEqual(resp.status_code, 200)
    def test_archives_content_with_post(self):
        now = datetime.datetime.now()
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        resp = self.client.get(reverse('spy:archives'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Post #1")
        self.assertContains(resp, reverse('spy:post_slug', args=(slugify(post_1.title),)))
        self.assertContains(resp, now.strftime("%Y-%m-%d"))
    def test_archives_content_with_posts(self):
        now1 = datetime.datetime.now()
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        now2 = datetime.datetime.now()
        user_2 = self.adduser('jane', 'doe@thebeatles.com')
        blogger_2 = self.addblogger(user_2, 2)
        post_2 = self.addpost(blogger_2, 'Post #2', 'body text for test2')
        resp = self.client.get(reverse('spy:archives'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Post #1")
        self.assertContains(resp, reverse('spy:post_slug', args=(slugify(post_1.title),)))
        self.assertContains(resp, now1.strftime("%Y-%m-%d, "))
        self.assertContains(resp, now1.strftime(":%M"))
        self.assertContains(resp, "by John:")
        self.assertContains(resp, "Post #2")
        self.assertContains(resp, reverse('spy:post_slug', args=(slugify(post_2.title),)))
        self.assertContains(resp, now2.strftime("%Y-%m-%d, "))
        self.assertContains(resp, now2.strftime(":%M"))
        self.assertContains(resp, "by Jane:")
    def test_archives_content_with_post_modified(self):
        now = datetime.datetime.now()
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        the_post = Post.objects.get(title='Post #1')
        the_post.title = 'Modified #1 Post'
        the_post.save()        
        resp = self.client.get(reverse('spy:archives'))
        self.assertEqual(resp.status_code, 200)
        self.assertNotContains(resp, "Post #1")
        self.assertContains(resp, "Modified #1 Post")
        self.assertContains(resp, reverse('spy:post_slug', args=(slugify(post_1.title),)))
        self.assertContains(resp, now.strftime("%Y-%m-%d"))
    def test_archives_content_with_posts_modified(self):
        now1 = datetime.datetime.now()
        user_1 = self.adduser('john', 'lennon@thebeatles.com')
        blogger_1 = self.addblogger(user_1, 1)
        post_1 = self.addpost(blogger_1, 'Post #1', 'body text for test')
        now2 = datetime.datetime.now()
        user_2 = self.adduser('jane', 'doe@thebeatles.com')
        blogger_2 = self.addblogger(user_2, 2)
        post_2 = self.addpost(blogger_2, 'Post #2', 'body text for test2')
        the_post = Post.objects.get(title='Post #1')
        the_post.title = 'Modified #1 Post'
        the_post.save()
        the_blogger2 = blogger_1
        the_post2 = Post.objects.get(title='Post #2')
        the_post2.blogger = the_blogger2
        the_post2.save()
        resp = self.client.get(reverse('spy:archives'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Modified #1 Post")
        self.assertContains(resp, reverse('spy:post_slug', args=(slugify(post_1.title),)))
        self.assertContains(resp, now1.strftime("%Y-%m-%d, "))
        self.assertContains(resp, now1.strftime(":%M"))
        self.assertContains(resp, "by John:")
        self.assertContains(resp, "Post #2")
        self.assertContains(resp, reverse('spy:post_slug', args=(slugify(post_2.title),)))
        self.assertContains(resp, now2.strftime("%Y-%m-%d, "))
        self.assertContains(resp, now2.strftime(":%M"))
        self.assertNotContains(resp, "by Jane:")

class BloggerModelTestCase(TestCase):
    def adduser(self, name, email):
        username = str(name)
        useremail = str(email)
        return User.objects.create_user(username, useremail, username+'password')
    def addblogger(self, user, avatar_number):
        username = user
        avatar_num = int(avatar_number)
        return Blogger.objects.create(
            user=username,
            avatar='default' + str(avatar_num)  + '.png'
        )
    def setUp(self):
        self.user_1 = self.adduser('john', 'lennon@thebeatles.com')
        self.blogger_1 = self.addblogger(self.user_1, 1)
        self.user_2 = self.adduser('jane', 'doe@thebeatles.com')
        self.blogger_2 = self.addblogger(self.user_2, 2)
    def test_str(self):
        self.assertEqual(self.blogger_1.__str__(), self.user_1.__str__())
        self.assertEqual(self.blogger_2.__str__(), self.user_2.__str__())
        self.assertEqual(self.blogger_1.__str__(), 'john')
        self.assertEqual(self.blogger_2.__str__(), 'jane')
    def test_upper_case_name(self):
        self.assertEqual(self.blogger_1.upper_case_name(), 'John')
        self.assertEqual(self.blogger_2.upper_case_name(), 'Jane')
    def test_avatar_thumb(self):
        self.assertEqual(self.blogger_1.avatar_thumb(), '<img src="/media/default1.png" width="100" />')
        self.assertEqual(self.blogger_2.avatar_thumb(), '<img src="/media/default2.png" width="100" />')

class PostModelTestCase(TestCase):
    def adduser(self, name, email):
        username = str(name)
        useremail = str(email)
        return User.objects.create_user(username, useremail, username+'password')
    def addblogger(self, user, avatar_number):
        username = user
        avatar_num = int(avatar_number)
        return Blogger.objects.create(
            user=username,
            avatar='default' + str(avatar_num)  + '.png'
        )
    def addpost(self, blogger, title, body):
        blogger = blogger
        title = str(title)
        body = str(body)
        slug = slugify(title)
        return Post.objects.create(
            blogger=blogger,
            title=title,
            body=body,
            slug=slug,
        )
    def setUp(self):
        self.user_1 = self.adduser('john', 'lennon@thebeatles.com')
        self.blogger_1 = self.addblogger(self.user_1, 1)
        self.user_2 = self.adduser('jane', 'doe@thebeatles.com')
        self.blogger_2 = self.addblogger(self.user_2, 2)
        self.post_1 = self.addpost(self.blogger_1, 'Post #1', 'body text for test1')
        self.post_2 = self.addpost(self.blogger_2, 'Post #2', 'body text for test2')
        self.post_3 = self.addpost(self.blogger_2, 'Post #3', 'body text for test3')
        self.post_4 = self.addpost(self.blogger_1, 'Post #4', 'body text for test4')
    def test_upper_case_name(self):
        self.assertEqual(self.post_1.upper_case_name(), 'John')
        self.assertEqual(self.post_2.upper_case_name(), 'Jane')
        self.assertEqual(self.post_3.upper_case_name(), 'Jane')
        self.assertEqual(self.post_4.upper_case_name(), 'John')
