from getnews.getDetail import getDetail
from headline import getHeadline


def renderHTMLNews(items):
    headline, now = getHeadline()
    header = (
        """ <html>
        <head>
            <title>{headline}</title>
            <meta http-equiv="content-type" content="text/html; charset=utf-8">
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
        """.format(
            headline=headline
        )
        + """
        <style>
            .title{
                font-size: 4vw; 
            }
            a, a:hover, a:focus, a:active {
                text-decoration: none;
                color: inherit;
                overflow: hidden;
        }
            img {
                    height: auto;

            }
            h5 {
                color:#356398;
                font-size: 3vw; 
            }
            p {
                font-size: 2vw; 
            }
            .col-md-5 { 
            padding : 0px;  
            height : 33vh;
                    overflow: hidden;
            display:flex;
            align-items: center;
            justify-content: center;
            }
            .card-text {
                    text-overflow : ellipsis;
                    -webkit-line-clamp: 3;
            }
        </style>
    </head>
    <body>
    """
        + """<p class="title" align="center"><b>{}</b></p> <br>""".format(headline)
    )

    footer = """
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
		<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
		<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
		<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
		<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
	</body>
</html>
"""
    with open("{}.html".format(now), "w", encoding="utf-8") as f:
        f.write(header)
        for item in items:
            link = item["link"].strip()
            title = item["title"].strip()
            print(title)
            detail = getDetail(link)
            if len(detail["description"]) > 100:
                detail["description"] = detail["description"][:100]
            contemp = """	
                <div class="card mb-3">
                <div class="row no-gutters">
                    <div class="col-md-5">
                        <img src="{image}" alt="{title1}">
                    </div>
                    <div class="col-md-7">
                        <div class="card-body">
                            <a href="{link}">
                            <h5 class="card-title">{title2}</h5>
                            <p class="card-text">{description}</p>
                            </a>
                        </div>
                    </div>
                </div>
                    </div>
                    
                """.format(
                link=link, image=detail["imgPath"], title1=title, title2=title, description=detail["description"]
            )
            f.write(contemp)
        f.write(footer)
