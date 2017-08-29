<!doctype html>
<html>
<head>
<meta charset="UTF-8">
<title>Roux Academy: Registration</title>
<link href="{{ asset('_css/main.css') }}" rel="stylesheet" media="screen, projection">
<meta name="viewport" content="initial-scale=1.0" />
</script>
</head>
<body id="blogPage">
<header class="blogHeader pageHeader">
  <h1>Roux Academy of Art and Design<a href="/index.htm" title="home"></a></h1>
  <nav id="pageNav" class="cf">
    <ul>
      <li><a href="_source/programs/programs.htm" title="programs">Programs</a></li>
      <li><a href="_source/admissions.htm" title="admissions">Admissions</a></li>
      <li><a href="_source/student_portal.htm" title="student portal">Student Portal</a></li>
      <li><a href="_source/campus_portal.htm" title="campus portal">Campus</a></li>
      <li><a href="_source/alumni.htm" title="alumni">Alumni</a></li>
      <li><a href="_source/blog/index.php"  title="Roux Academy Official Blog">Blog</a></li>
      <li><a href="_source/about/about.htm"  title="about Roux Academy">About</a></li>
    </ul>
  </nav>
</header>
<div id="contentWrapper">
  <article id="mainContent">
    <h1>Sign Up!</h1>
    <article class="post">
      <h2>New User Registration</h2>
      <!-- form goes here -->
      {{ Form::open(array('url' => 'register')) }}
        {{ Form::label('email', 'Email address') }}
        {{ Form::text('email') }}

        {{ Form::label('username', 'Username') }}
        {{ Form::text('username') }}

        {{ Form::label('password', 'Password') }}
        {{ Form::password('password') }}

        {{ Form::submit('Sign Up') }}
      {{ Form::close() }}
</article>
  </article>
  <aside>
    <section class="info">
      <div class="widget">
        <h2>Search</h2>
        <form>
          <input type="search" id="searchField" placeholder="Enter keyword(s)" />
          <input type="submit" name="search" id="search" value="">
        </form>
      </div>
      <div class="widget">
        <h2>Hot Links</h2>
        <ul>
          <li><a href="#">Conference Schedule-At-A-Glance</a></li>
          <li><a href="#">Another Page Title</a></li>
          <li><a href="#">Yet Another Page Title</a></li>
        </ul>
      </div>
      <div class="widget">
        <h2>Archive</h2>
        <ul>
          <li><a href="#">September</a></li>
          <li><a href="#">August</a></li>
          <li><a href="#">July</a></li>
          <li><a href="#">June</a></li>
        </ul>
      </div>
      <div class="widget">
        <h2>Categories</h2>
        <ul>
          <li><a href="#">Conference</a></li>
          <li><a href="#">Events</a></li>
          <li><a href="#">Student Life</a></li>
          <li><a href="#">Zeitgeist</a></li>
        </ul>
      </div>
    </section>
  </aside>
</div>
<footer id="pageFooter" class="cf">
  <nav class="footerNav">
    <section class="col">
      <h3>About Roux Academy</h3>
      <div class="col1">
        <ul>
          <li><a href="_source/mission.htm" title="Our mission">Mission Statement</a></li>
          <li><a href="_source/history.htm" title="school history">School History</a></li>
          <li><a href="_source/accreditation.htm" title="accreditation and affliates">Accreditation &amp; Affiliates</a></li>
          <li><a href="_source/board.htm" title="board members">Board Members</a></li>
        </ul>
      </div>
      <div class="col2">
        <ul>
          <li><a href="_source/faculty.htm" title="faculty and staff">Faculty &amp; Staff</a></li>
          <li><a href="_source/visiting_professors.htm" title="visiting professors">Visiting Professors</a></li>
          <li><a href="_source/museum.htm" title="Maribielle Roux Museum">Marbielle Roux Museum</a></li>
          <li><a href="_source/directions.htm" title="directions">Map &amp; Directions</a></li>
        </ul>
      </div>
    </section>
    <section class="col">
      <h3>Admissions &amp; Programs</h3>
      <div class="col1">
        <ul>
          <li><a href="_source/degrees.htm" title="Degree programs">Degree Programs</a></li>
          <li><a href="_source/catalog.htm" title="course catalog">Course Catalog</a></li>
          <li><a href="_source/fine_art.htm" title="fine art programs">Fine Art Programs</a></li>
          <li><a href="_source/design.htm" title="design concentration">Design Concentration</a></li>
        </ul>
      </div>
      <div class="col2">
        <ul>
          <li><a href="_source/fashion.htm" title="fashion program">Fashion Program</a></li>
          <li><a href="_source/product_design.htm" title="product design">Product Design</a></li>
          <li><a href="_source/continuing_ed.htm" title="Continuing Education">Continuing Education</a></li>
          <li><a href="_source/financial_aid.htm" title="tuition and financial aid">Tuition &amp; Financial Aid</a></li>
        </ul>
      </div>
    </section>
    <section class="col">
      <h3>Student Resources</h3>
      <div class="col1">
        <ul>
          <li><a href="_source/campus.htm" title="Campus information">Campus Information</a></li>
          <li><a href="_source/housing.htm" title="student housing">Student Housing</a></li>
          <li><a href="_source/contact.htm" title="transcript request">Transcript Request</a></li>
          <li><a href="_source/applying.htm" title="application process">Application Process</a></li>
        </ul>
      </div>
      <div class="col2">
        <ul>
          <li><a href="_source/portfolio_review.htm" title="portfolio review">Portfolio Review</a></li>
          <li><a href="_source/conselling.htm" title="career counselling">Career Counselling</a></li>
          <li><a href="_source/internships.htm" title="internship programs">Internship Programs</a></li>
          <li><a href="_source/student_portal.htm" title="student portal login">Student Portal Login</a></li>
        </ul>
      </div>
    </section>
  </nav>
  <p>&copy;Copyright  Roux Academy of Art &amp; Design.  All rights reserved. <a href="_source/privacy.htm" title="privacy statement">Privacy Statement</a> |<a href="_source/legal.htm" title="legal terms"> Legal Terms and Conditions</a> |<a href="_source/disclosures.htm" title="student outcomes and disclosures"> Student Outcomes/Disclosures</a></p>
</footer>
</body>
</html>
