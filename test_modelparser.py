import unittest
import morango.modelparser as modelparser
import morango.exceptions as exceptions

class TestBlog(unittest.TestCase):
  def test_parse(self):
    """
    Tests that the blog.mdl file is parsed correctly
    """
    MSINGLE = modelparser.MULT_SINGLE
    MANY = modelparser.MULT_ANY
    # TODO: finish this
    exp_post = {
      'fields': [
        {'name':'', 'type':'', 'mult':MSINGLE},
      ]
    }
    blog = modelparser.parse('test/blog.mdl')
    print(blog)
    self.assertEqual(len(blog), 3) # 3 models
    # be sure we parsed all the models
    self.assertEqual(blog[0]['model'], 'Post')
    self.assertEqual(blog[1]['model'], 'Tag')
    self.assertEqual(blog[2]['model'], 'Author')
    post_mdl = blog[0]
    # assert all post fields were parsed
    self.assertEqual(len(post_mdl['fields']), 5)
    # TODO: assert more stuff

  def test_repeated_definitions(self):
    """
    Tests that a model with repeated model definitions
    is not ok.
    """
    self.assertRaises(exceptions.ModelNotUnique, 
    	modelparser.parse_files,
    	['test/repeated.mdl'])

if __name__ == '__main__':
  unittest.main()