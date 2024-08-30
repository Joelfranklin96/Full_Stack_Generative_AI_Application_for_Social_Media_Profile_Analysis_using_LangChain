from click import prompt
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_parties.twitter import scrape_user_tweets
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parsers import summary_parser, Summary


def ice_break_with(name: str) -> tuple[Summary, str]:
    linkedin_user_name = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_user_name, mock=True)

    twitter_user_name = twitter_lookup_agent(name)
    tweets = scrape_user_tweets(username=twitter_user_name, num_tweets=5, mock=True)

    summary_template = """
        given the information about a person from linkedin {information},
        and their latest twitter posts {twitter_posts} I want you to create:
        1. A short summary
        2. two interesting facts about them 

        Use both information from twitter and Linkedin
        \n{format_instructions}
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"], template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        }
    )
    #'information' and 'twitter_posts' are defined when the chain is invoked whereas the 'partial_variables' are pre-defined even before the chain is invoked.

    # 'format_instructions' do not dynamically depend on the actual 'summary' and 'facts content'. Instead, they are predefined instructions that specify the format in which the LLM should produce its output.

    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    llm = ChatOpenAI(model="gpt-3.5-turbo")

    #chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    # chain = summary_prompt_template | llm | StrOutputParser()
    # Think of the 'pipe operator' as the one making an api call to the LLM.
    # StrOutputParser() cleans up the text we get from LLM.

    chain = summary_prompt_template | llm | summary_parser
    # The summary_prompt_template is fed into the llm and then the output of llm is fed into summary_parser

    res = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    print(res)
    print(res.summary)
    print(res.facts)

    return res, linkedin_data.get("profile_pic_url")


if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker Enter")
    ice_break_with(name="Eden Marco Udemy")
