from igloo.models.user import User
from igloo.models.access_token import AccessToken
from igloo.models.pending_share import PendingShare
from igloo.models.collection import Collection
from igloo.models.thing import Thing
from igloo.models.variable import Variable
from igloo.models.float_variable import FloatVariable
from igloo.models.pending_transfer import PendingTransfer
from igloo.models.notification import Notification
from igloo.models.boolean_variable import BooleanVariable
from igloo.models.string_variable import StringVariable
from igloo.models.float_series_variable import FloatSeriesVariable
from igloo.models.category_series_variable import CategorySeriesVariable
from igloo.models.category_series_node import CategorySeriesNode
from igloo.models.float_series_node import FloatSeriesNode
from igloo.utils import parse_arg, undefined


async def _asyncWrapWith(res, wrapper_fn):
    result = await res
    return wrapper_fn(result["id"])


def wrapById(res, wrapper_fn):
    if isinstance(res, dict):
        return wrapper_fn(res["id"])
    else:
        return _asyncWrapWith(res, wrapper_fn)


def wrapWith(res, wrapper_fn):
    if isinstance(res, dict):
        return wrapper_fn(res)
    else:
        return _asyncWrapWith(res, wrapper_fn)


class MutationRoot:
    def __init__(self, client):
        self.client = client

    def sendConfirmationEmail(self, email, operation):
        email_arg = parse_arg("email", email)
        operation_arg = parse_arg("operation", operation, is_enum=True)

        return self.client.mutation('mutation{sendConfirmationEmail(%s%s)}' % (email_arg, operation_arg))["sendConfirmationEmail"]

    async def _wrapLogIn(self, res):
        resDict = await res
        resDict["user"] = User(self.client)
        return resDict

    def log_in(self, email, password, totp=undefined, private_cloud=undefined):
        email_arg = parse_arg("email", email)
        password_arg = parse_arg("password", password)
        totp_arg = parse_arg("totp", totp)
        privateCloud_arg = parse_arg("privateCloud", private_cloud)

        res = self.client.mutation('mutation{logIn(%s%s%s%s){user{id} token}}' % (email_arg,
                                                                                  password_arg,
                                                                                  totp_arg,
                                                                                  privateCloud_arg))["logIn"]

        if isinstance(res, dict):
            self.client.set_token(res["token"])
            res["user"] = User(self.client)
            return res
        else:
            return self._wrapLogIn(res)

    def create_access_token(self, name, password):
        name_arg = parse_arg("name", name)
        password_arg = parse_arg("password", password)
        return self.client.mutation('mutation{createAccessToken(%s%s)}' % (name_arg, password_arg))["createAccessToken"]

    def regenerate_access_token(self, id, password):
        id_arg = parse_arg("id", id)
        password_arg = parse_arg("password", password)

        return self.client.mutation('mutation{regenerateAccessToken(%s%s)}' % (id_arg, password_arg))["regenerateAccessToken"]

    def delete_access_token(self, id, password):
        id_arg = parse_arg("id", id)
        password_arg = parse_arg("password", password)

        return self.client.mutation('mutation{deleteAccessToken(%s%s)}' % (id_arg, password_arg))["deleteAccessToken"]

    async def _wrapSignUp(self, res):
        result = await res
        result["user"] = User(self.client)

        return result

    def sign_up(self, email, name, password, accept_privacy_policy, private_cloud=undefined):
        email_arg = parse_arg("email", email)
        name_arg = parse_arg("name", name)
        password_arg = parse_arg("password", password)
        privateCloud_arg = parse_arg("privateCloud", private_cloud)
        acceptPrivacyPolicy_arg = parse_arg(
            "acceptPrivacyPolicy", accept_privacy_policy)

        res = self.client.mutation('mutation{signUp(%s%s%s%s%s){user{id} token}}' % (
            email_arg,
            name_arg,
            password_arg,
            privateCloud_arg,
            acceptPrivacyPolicy_arg))["signUp"]

        if isinstance(res, dict):
            res["user"] = User(self.client, res["user"]["id"])
            return res
        else:
            return self._wrapSignUp(res)

    def accept_legal_documents(self, privacy_policy=undefined):
        privacy_policy_arg = parse_arg(
            "privacyPolicy", privacy_policy)
        res = self.client.mutation("mutation{acceptLegalDocuments(%s) }" % privacy_policy_arg)[
            "acceptLegalDocuments"]

        return res

    def initiate_billing_setup(self):
        res = self.client.mutation("mutation{initiateBillingSetup }")[
            "initiateBillingSetup"]

        return res

    def update_payment_method(self, stripe_payment_method):
        stripePaymentMethod_arg = parse_arg(
            "stripePaymentMethod", stripe_payment_method)
        res = self.client.mutation("mutation{updatePaymentMethod(%s) }" % stripePaymentMethod_arg)[
            "updatePaymentMethod"]

        return res

    def confirm_payment_execution(self):
        res = self.client.mutation("mutation{confirmPaymentExecution }")[
            "confirmPaymentExecution"]

        return res

    def retry_payment(self):
        res = self.client.mutation("mutation{retryPayment }")[
            "retryPayment"]

        return res

    # def change_billing_plan(self, billing_plan, billing_cycle, extra_storage, extra_throughput, custom_apps):
    #     billingPlan_arg = parse_arg("billingPlan", billing_plan, is_enum=True)
    #     billingCycle_arg = parse_arg(
    #         "billingCycle", billing_cycle, is_enum=True)
    #     extraStorage_arg = parse_arg("extraStorage", extra_storage)
    #     extraThroughput_arg = parse_arg("extraThroughput", extra_throughput)
    #     customApps_arg = parse_arg("customApps", custom_apps)

    #     res = self.client.mutation("mutation{changeBillingPlan(%s%s%s%s%s) }" % (
    #         billingPlan_arg,
    #         billingCycle_arg,
    #         extraStorage_arg,
    #         extraThroughput_arg,
    #         customApps_arg
    #     ))[
    #         "changeBillingPlan"]

    #     return res

    def change_password(self, new_password, old_password):
        new_password_arg = parse_arg("newPassword", new_password)
        old_password_arg = parse_arg("oldPassword", old_password)

        res = self.client.mutation(
            'mutation{changePassword(%s%s)}' % (new_password_arg, old_password_arg))["changePassword"]

        return res

    def set_totp(self, totp, secret, password):
        totp_arg = parse_arg("totp", totp)
        secret_arg = parse_arg("secret", secret)
        password_arg = parse_arg("password", password)
        return self.client.mutation('mutation{setTotp(%s%s%s)}' % (totp_arg, secret_arg, password_arg))["setTotp"]

    def disable_totp(self, password):
        password_arg = parse_arg("password", password)
        return self.client.mutation('mutation{disableTotp(%s%s%s)}' % password_arg)["disableTotp"]

    def send_disable_totp_email(self, email, redirect_to):
        email_arg = parse_arg("email", email)
        redirect_to_arg = parse_arg("redirectTo", redirect_to, is_enum=True)
        return self.client.mutation('mutation{sendDisableTotpEmail(%s%s)}' % (email_arg, redirect_to_arg))["sendDisableTotpEmail"]

    def send_verification_email(self, redirect_to):
        redirect_to_arg = parse_arg("redirectTo", redirect_to, is_enum=True)

        return self.client.mutation('mutation{sendVerificationEmail(%s)}' % (redirect_to_arg))["sendVerificationEmail"]

    def send_password_recovery_email(self, email, redirect_to):
        email_arg = parse_arg("email", email)
        redirect_to_arg = parse_arg("redirectTo", redirect_to, is_enum=True)
        return self.client.mutation('mutation{sendPasswordRecoveryEmail(%s%s)}' % (email_arg, redirect_to_arg))["sendPasswordRecoveryEmail"]

    def reset_password(self, recovery_token, new_password):
        recovery_token_arg = parse_arg("recoveryToken", recovery_token)
        new_password_arg = parse_arg("newPassword", new_password)
        return self.client.mutation('mutation{resetPassword(%s%s)}' % (recovery_token_arg, new_password_arg))["resetPassword"]

    def share_collection(self, collection_id, role, email=undefined, user_id=undefined):
        collectionId_arg = parse_arg("collectionId", collection_id)
        role_arg = parse_arg("role", role, is_enum=True)
        email_arg = parse_arg("email", email)
        userId_arg = parse_arg("userId", user_id)
        res = self.client.mutation('mutation{shareCollection(%s%s%s%s){id}}' % (
            collectionId_arg, email_arg, userId_arg, role_arg))["shareCollection"]

        def wrapper(id):
            return PendingShare(self.client, id)

        return wrapById(res, wrapper)

    def pending_share(self, id, role):
        id_arg = parse_arg("id", id)
        role_arg = parse_arg("role", role, is_enum=True)

        res = self.client.mutation('mutation{pendingShare(%s%s){id}}' % (
            id_arg, role_arg))["pendingShare"]

        def wrapper(id):
            return PendingShare(self.client, id)

        return wrapById(res, wrapper)

    def revoke_pending_share(self, id):
        id_arg = parse_arg(
            "id", id)

        return self.client.mutation('mutation{revokePendingShare(%s)}' % (id_arg))["revokePendingShare"]

    def accept_pending_share(self, id):
        id_arg = parse_arg(
            "pendingShareId", id)

        res = self.client.mutation('mutation{acceptPendingShare(%s){sender{id} recipient{id} role collection{id}}}' % (
            id_arg))["acceptPendingShare"]

        def wrapper(res):
            res["sender"] = User(self.client, res["sender"]["id"])
            res["recipient"] = User(self.client, res["recipient"]["id"])
            res["collection"] = Collection(
                self.client, res["collection"]["id"])

            return res

        return wrapWith(res, wrapper)

    def decline_pending_share(self, id):
        id_arg = parse_arg(
            "id", id)

        return self.client.mutation('mutation{declinePendingShare(%s)}' % (id_arg))["declinePendingShare"]

    def stop_sharing_collection(self, collection_id, email=undefined, user_id=undefined):
        collectionId_arg = parse_arg("collectionId", collection_id)
        email_arg = parse_arg("email", email)
        userId_arg = parse_arg("userId", user_id)
        res = self.client.mutation('mutation{stopSharingCollection(%s%s%s){id}}' % (
            collectionId_arg, email_arg, userId_arg))["stopSharingCollection"]

        def wrapper(id):
            return Collection(self.client, id)

        return wrapById(res, wrapper)

    def leave_collection(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{leaveCollection(%s)}' % (id_arg))["leaveCollection"]

    def transfer_collection(self, collection_id, email=undefined, user_id=undefined):
        collectionId_arg = parse_arg("collectionId", collection_id)
        email_arg = parse_arg("email", email)
        userId_arg = parse_arg("userId", user_id)
        res = self.client.mutation('mutation{transferCollection(%s%s%s){id}}' % (
            collectionId_arg, email_arg, userId_arg))["transferCollection"]

        def wrapper(id):
            return PendingTransfer(self.client, id)

        return wrapById(res, wrapper)

    def revoke_pending_transfer(self, id):
        id_arg = parse_arg(
            "id", id)

        return self.client.mutation('mutation{revokePendingTransfer(%s)}' % (id_arg))["revokePendingTransfer"]

    def accept_pending_transfer(self, id):
        id_arg = parse_arg(
            "id", id)

        res = self.client.mutation('mutation{acceptPendingTransfer(%s){id sender{id} recipient{id} collection{id}}}' % (
            id_arg))["acceptPendingTransfer"]

        def wrapper(res):
            res["sender"] = User(self.client, res["sender"]["id"])
            res["recipient"] = User(self.client, res["recipient"]["id"])
            res["collection"] = Collection(
                self.client, res["collection"]["id"])

            return res

        return wrapWith(res, wrapper)

    def decline_pending_transfer(self, id):
        id_arg = parse_arg(
            "id", id)

        return self.client.mutation('mutation{declinePendingTransfer(%s)}' % (id_arg))["declinePendingTransfer"]

    def change_role(self, collection_id, new_role, email=undefined, user_id=undefined):
        collectionId_arg = parse_arg("collectionId", collection_id)
        email_arg = parse_arg("email", email)
        user_id_arg = parse_arg("userId", user_id)
        newRole_arg = parse_arg("newRole", new_role)

        res = self.client.mutation('mutation{changeRole(%s%s%s%s){id}}' % (
            collectionId_arg, newRole_arg, user_id_arg, email_arg))["changeRole"]

        def wrapper(id):
            return Collection(self.client, id)

        return wrapById(res, wrapper)

    def create_collection(self, name, picture=undefined, index=undefined, muted=undefined):
        name_arg = parse_arg("name", name)
        picture_arg = parse_arg("picture", picture, is_enum=True)
        index_arg = parse_arg("index", index)
        muted_arg = parse_arg("muted", muted)
        res = self.client.mutation('mutation{createCollection(%s%s%s%s){id}}' % (
            name_arg, picture_arg, index_arg, muted_arg))["createCollection"]

        def wrapper(id):
            return Collection(self.client, id)

        return wrapById(res, wrapper)

    def create_thing(self, type, firmware=undefined, stored_notifications=undefined):
        type_arg = parse_arg("type", type)
        firmware_arg = parse_arg("firmware", firmware)
        stored_notifications_arg = parse_arg(
            "storedNotifications", stored_notifications)
        res = self.client.mutation('mutation{createThing(%s%s%s){id}}' % (
            type_arg, firmware_arg, stored_notifications_arg))["createThing"]

        # FIXME: if we choose to keep the createThingPayload implement it here
        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def pair_thing(self, pair_code, name, collection_id, index=undefined):
        pairCode_arg = parse_arg("pairCode", pair_code)
        name_arg = parse_arg("name", name)
        collectionId_arg = parse_arg("collectionId", collection_id)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{pairThing(%s%s%s%s){id}}' % (
            pairCode_arg, name_arg, index_arg, collectionId_arg))["pairThing"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def create_notification(self, thing_id, content, timestamp=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        content_arg = parse_arg("content", content)
        timestamp_arg = parse_arg("timestamp", timestamp)
        res = self.client.mutation('mutation{createNotification(%s%s%s){id}}' % (
            thingId_arg, content_arg, timestamp_arg))["createNotification"]

        def wrapper(id):
            return Notification(self.client, id)

        return wrapById(res, wrapper)

    def create_float_variable(self, user_permission, name, thing_id=undefined, developer_only=undefined, allowed_values=undefined, unit_of_measurement=undefined, value=undefined, precision=undefined, min=undefined, max=undefined, index=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        user_permission_arg = parse_arg(
            "userPermission", user_permission, is_enum=True)
        name_arg = parse_arg("name", name)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        allowed_values_arg = parse_arg("hidden", allowed_values)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unit_of_measurement)
        value_arg = parse_arg("value", value)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createFloatVariable(%s%s%s%s%s%s%s%s%s%s%s){id}}' % (thingId_arg, user_permission_arg, allowed_values_arg, developer_only_arg,
                                                                                                  unitOfMeasurement_arg, value_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["createFloatVariable"]

        def wrapper(id):
            return FloatVariable(self.client, id)

        return wrapById(res, wrapper)

    def create_string_variable(self, user_permission, name, thing_id=undefined, developer_only=undefined, value=undefined, max_characters=undefined, allowed_values=undefined, index=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        user_permission_arg = parse_arg(
            "userPermission", user_permission, is_enum=True)
        name_arg = parse_arg("name", name)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        value_arg = parse_arg("value", value)
        maxChars_arg = parse_arg("maxChars", max_characters)

        allowedValues_arg = parse_arg("allowedValues", allowed_values)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createStringVariable(%s%s%s%s%s%s%s%s){id}}' % (
            thingId_arg, user_permission_arg, developer_only_arg, value_arg, maxChars_arg, name_arg, allowedValues_arg, index_arg))["createStringVariable"]

        def wrapper(id):
            return StringVariable(self.client, id)

        return wrapById(res, wrapper)

    def create_boolean_variable(self, user_permission, name, thing_id=undefined, developer_only=undefined,  value=undefined, index=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        user_permission_arg = parse_arg(
            "userPermission", user_permission, is_enum=True)
        name_arg = parse_arg("name", name)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        value_arg = parse_arg("value", value)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createBooleanVariable(%s%s%s%s%s%s){id}}' % (
            thingId_arg, user_permission_arg, developer_only_arg, value_arg, name_arg, index_arg))["createBooleanVariable"]

        def wrapper(id):
            return BooleanVariable(self.client, id)

        return wrapById(res, wrapper)

    def create_float_series_variable(self, name, shown_nodes=undefined, thing_id=undefined, developer_only=undefined, unit_of_measurement=undefined, precision=undefined, min=undefined, max=undefined, index=undefined, stored_nodes=undefined):
        thingId_arg = parse_arg("thingId", thing_id)
        name_arg = parse_arg("name", name)
        developer_only_arg = parse_arg("private", developer_only)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unit_of_measurement)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)
        shown_nodes_arg = parse_arg("max", shown_nodes)
        stored_nodes_arg = parse_arg("max", stored_nodes)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{createFloatSeriesVariable(%s%s%s%s%s%s%s%s%s%s){id}}' % (
            shown_nodes_arg, stored_nodes_arg, thingId_arg, developer_only_arg, unitOfMeasurement_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["createFloatSeriesVariable"]

        def wrapper(id):
            return FloatSeriesVariable(self.client, id)

        return wrapById(res, wrapper)

    def create_float_series_node(self, series_id, value=undefined, timestamp=undefined):
        seriesId_arg = parse_arg("seriesId", series_id)
        value_arg = parse_arg("value", value)
        timestamp_arg = parse_arg("timestamp", timestamp)
        res = self.client.mutation('mutation{createFloatSeriesNode(%s%s%s){id}}' % (
            seriesId_arg, timestamp_arg, value_arg))["createFloatSeriesNode"]

        def wrapper(id):
            return FloatSeriesNode(self.client, id)

        return wrapById(res, wrapper)

    def update_user(self,
                    company_name=undefined,
                    quiet_mode=undefined,
                    name=undefined,
                    vat_number=undefined,
                    lenght_and_mass=undefined,
                    temperature=undefined,
                    date_format=undefined,
                    time_format=undefined,
                    password_change_email=undefined,
                    shares_email=undefined,
                    access_token_created_email=undefined,
                    address_line1=undefined,
                    address_line2=undefined,
                    address_postal_code=undefined,
                    address_city=undefined,
                    address_state=undefined,
                    address_country_or_territory=undefined,
                    language=undefined
                    ):

        company_name_arg = parse_arg("companyName", company_name)
        language_arg = parse_arg("language", language)
        quiet_mode_arg = parse_arg("quietMode", quiet_mode)
        name_arg = parse_arg("name", name)
        vat_number_arg = parse_arg("vatNumber", vat_number)
        lenght_and_mass_arg = parse_arg(
            "lenghtAndMass", lenght_and_mass)
        temperature_arg = parse_arg("temperature", temperature)
        date_format_arg = parse_arg("dateFormat", date_format)
        time_format_arg = parse_arg("timeFormat", time_format)
        password_change_email_arg = parse_arg(
            "passwordChangeEmail", password_change_email)
        shares_email_arg = parse_arg("sharesEmail", shares_email)
        access_token_created_email_arg = parse_arg(
            "accessTokenCreatedEmail", access_token_created_email)
        address_line1_arg = parse_arg("addressLine1", address_line1)
        address_line2_arg = parse_arg("addressLine2", address_line2)
        address_postal_code_arg = parse_arg(
            "addressPostalCode", address_postal_code)
        address_city_arg = parse_arg("addressCity", address_city)
        address_state_arg = parse_arg("addressState", address_state)
        address_country_or_territory_arg = parse_arg(
            "addressCountryOrTerritory", address_country_or_territory)

        res = self.client.mutation('mutation{updateUser(%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            company_name_arg, quiet_mode_arg, name_arg, vat_number_arg, lenght_and_mass_arg, temperature_arg, date_format_arg, time_format_arg, password_change_email_arg, shares_email_arg, access_token_created_email_arg, address_line1_arg, address_line2_arg, address_postal_code_arg, address_city_arg, address_state_arg, address_country_or_territory_arg, language_arg
        ))["updateUser"]

        def wrapper(id):
            return User(self.client)

        return wrapById(res, wrapper)

    def change_email(self, newEmail, password, redirect_to):
        newEmail_arg = parse_arg("newEmail", newEmail)
        password_arg = parse_arg("password", password)
        redirect_to_arg = parse_arg("redirectTo", redirect_to)

        return self.client.mutation('mutation{changeEmail(%s%s%s)}' % (newEmail_arg, password_arg, redirect_to_arg))["changeEmail"]

    def update_collection(self, id, name=undefined, picture=undefined, index=undefined, muted=undefined):
        id_arg = parse_arg("id", id)
        name_arg = parse_arg("name", name)
        picture_arg = parse_arg("picture", picture, is_enum=True)
        index_arg = parse_arg("index", index)
        muted_arg = parse_arg("muted", muted)
        res = self.client.mutation('mutation{updateCollection(%s%s%s%s%s){id}}' % (
            id_arg, name_arg, picture_arg, index_arg, muted_arg))["updateCollection"]

        def wrapper(id):
            return Collection(self.client, id)

        return wrapById(res, wrapper)

    def update_thing(self, id, online=undefined, type=undefined, name=undefined, index=undefined, signal=undefined, battery=undefined, battery_charging=undefined, firmware=undefined, muted=undefined, starred=undefined, stored_notifications=undefined):
        id_arg = parse_arg("id", id)
        thingType_arg = parse_arg("type", type)
        name_arg = parse_arg("name", name)
        index_arg = parse_arg("index", index)
        signal_arg = parse_arg("signal", signal)
        battery_arg = parse_arg("battery", battery)
        batteryCharging_arg = parse_arg("batteryCharging", battery_charging)
        firmware_arg = parse_arg("firmware", firmware)
        muted_arg = parse_arg("muted", muted)
        starred_arg = parse_arg("starred", starred)
        online_arg = parse_arg("online", online)
        stored_notifications_arg = parse_arg(
            "storedNotifications", stored_notifications)
        res = self.client.mutation('mutation{updateThing(%s%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            online_arg, stored_notifications_arg, id_arg, thingType_arg, name_arg, index_arg, signal_arg, battery_arg, batteryCharging_arg, firmware_arg, muted_arg, starred_arg))["updateThing"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def move_thing(self, thing_id, new_collection_id):
        thing_id_arg = parse_arg("thingId", thing_id)
        new_collection_id_arg = parse_arg(
            "newCollectionId", new_collection_id)

        res = self.client.mutation('mutation{moveThing(%s%s){id}}' % (
            thing_id_arg, new_collection_id_arg))["moveThing"]

        def wrapper(id):
            return Thing(self.client, id)

        return wrapById(res, wrapper)

    def variable(self, id, developer_only=undefined, hidden=undefined, name=undefined, index=undefined):
        id_arg = parse_arg("id", id)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)

        name_arg = parse_arg("name", name)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{updateVariable(%s%s%s%s%s){id __typename}}' % (
            id_arg, developer_only_arg, hidden_arg, name_arg, index_arg))["updateFloatVariable"]

        def wrapper(res):
            return Variable(self.client, res["id"], res["__typename"])

        return wrapWith(res, wrapper)

    def update_float_variable(self, id, user_permission=undefined, developer_only=undefined, hidden=undefined, unit_of_measurement=undefined, value=undefined, precision=undefined, min=undefined, max=undefined, name=undefined, index=undefined, allowed_values=undefined):
        id_arg = parse_arg("id", id)
        user_permission_arg = parse_arg(
            "userPermission", user_permission, is_enum=True)
        developer_only_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)
        unit_of_measurement_arg = parse_arg(
            "unitOfMeasurement", unit_of_measurement)
        value_arg = parse_arg("value", value)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)
        name_arg = parse_arg("name", name)
        allowed_values_arg = parse_arg("allowedValues", allowed_values)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{updateFloatVariable(%s%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, user_permission_arg, developer_only_arg, allowed_values_arg, hidden_arg, unit_of_measurement_arg, value_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["updateFloatVariable"]

        def wrapper(id):
            return FloatVariable(self.client, id)

        return wrapById(res, wrapper)

    def increment_float_variable(self, id, increment_by):
        id_arg = parse_arg("id", id)
        incrementBy_arg = parse_arg("incrementBy", increment_by)

        res = self.client.mutation('mutation{incrementFloatVariable(%s%s){id}}' % (
            id_arg, incrementBy_arg))["incrementFloatVariable"]

        def wrapper(id):
            return FloatVariable(self.client, id)

        return wrapById(res, wrapper)

    def update_string_variable(self, id, user_permission=undefined, developer_only=undefined, hidden=undefined, value=undefined, max_characters=undefined, name=undefined, allowed_values=undefined, index=undefined):
        id_arg = parse_arg("id", id)
        user_permission_arg = parse_arg(
            "userPermission", user_permission, is_enum=True)
        private_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        maxChars_arg = parse_arg("maxCharacters", max_characters)
        name_arg = parse_arg("name", name)

        allowedValues_arg = parse_arg("allowedValues", allowed_values)
        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{updateStringVariable(%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, user_permission_arg, private_arg, hidden_arg, value_arg, maxChars_arg, name_arg, allowedValues_arg, index_arg))["updateStringVariable"]

        def wrapper(id):
            return StringVariable(self.client, id)

        return wrapById(res, wrapper)

    def update_boolean_variable(self, id, user_permission=undefined, developer_only=undefined, hidden=undefined, value=undefined, name=undefined, index=undefined):
        id_arg = parse_arg("id", id)
        user_permission_arg = parse_arg(
            "userPermission", user_permission, is_enum=True)
        private_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)
        value_arg = parse_arg("value", value)
        name_arg = parse_arg("name", name)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{updateBooleanVariable(%s%s%s%s%s%s%s){id}}' % (
            id_arg, user_permission_arg, private_arg, hidden_arg, value_arg, name_arg, index_arg))["updateBooleanVariable"]

        def wrapper(id):
            return BooleanVariable(self.client, id)

        return wrapById(res, wrapper)

    def update_float_series_variable(self, id, developer_only=undefined, hidden=undefined, unit_of_measurement=undefined, precision=undefined, min=undefined, max=undefined, name=undefined, index=undefined, shown_nodes=undefined, stored_nodes=undefined):
        id_arg = parse_arg("id", id)
        private_arg = parse_arg("developerOnly", developer_only)
        hidden_arg = parse_arg("hidden", hidden)
        unitOfMeasurement_arg = parse_arg(
            "unitOfMeasurement", unit_of_measurement)
        precision_arg = parse_arg("precision", precision)
        min_arg = parse_arg("min", min)
        max_arg = parse_arg("max", max)
        name_arg = parse_arg("name", name)
        shown_nodes_arg = parse_arg("shownNodes", shown_nodes)
        stored_nodes_arg = parse_arg("storedNodes", stored_nodes)

        index_arg = parse_arg("index", index)
        res = self.client.mutation('mutation{updateFloatSeriesVariable(%s%s%s%s%s%s%s%s%s%s%s){id}}' % (
            id_arg, private_arg, shown_nodes_arg, stored_nodes_arg, hidden_arg, unitOfMeasurement_arg, precision_arg, min_arg, max_arg, name_arg, index_arg))["updateFloatSeriesVariable"]

        def wrapper(id):
            return FloatSeriesVariable(self.client, id)

        return wrapById(res, wrapper)

    def update_float_series_node(self, id, value=undefined, timestamp=undefined):
        id_arg = parse_arg("id", id)
        value_arg = parse_arg("value", value)
        timestamp_arg = parse_arg("timestamp", timestamp)
        res = self.client.mutation('mutation{updateFloatSeriesNode(%s%s%s){id}}' % (
            id_arg, value_arg, timestamp_arg))["updateFloatSeriesNode"]

        def wrapper(id):
            return FloatSeriesNode(self.client, id)

        return wrapById(res, wrapper)

    # def category_series_variable(self, id, developer_only=undefined, hidden=undefined, name=undefined, allowed_values=undefined, index=undefined, shown_nodes=undefined, stored_nodes=undefined):
    #     id_arg = parse_arg("id", id)
    #     developer_only_arg = parse_arg("developerOnly", developer_only)
    #     hidden_arg = parse_arg("hidden", hidden)
    #     name_arg = parse_arg("name", name)
    #     shown_nodes_arg = parse_arg("shownNodes", shown_nodes)
    #     stored_nodes_arg = parse_arg("storedNodes", stored_nodes)

    #     allowedValues_arg = parse_arg("allowedValues", allowed_values)
    #     index_arg = parse_arg("index", index)
    #     res = self.client.mutation('mutation{categorySeriesVariable(%s%s%s%s%s%s%s%s){id}}' % (
    #         id_arg, developer_only_arg, shown_nodes_arg, stored_nodes_arg, hidden_arg, name_arg, allowedValues_arg, index_arg))["categorySeriesVariable"]

    #     def wrapper(id):
    #         return CategorySeriesVariable(self.client, id)

    #     return wrapById(res, wrapper)

    # def category_series_node(self, id, value=undefined, timestamp=undefined):
    #     id_arg = parse_arg("id", id)
    #     value_arg = parse_arg("value", value)
    #     timestamp_arg = parse_arg("timestamp", timestamp)
    #     res = self.client.mutation('mutation{categorySeriesNode(%s%s%s){id}}' % (
    #         id_arg, value_arg, timestamp_arg))["categorySeriesNode"]

    #     def wrapper(id):
    #         return CategorySeriesNode(self.client, id)

    #     return wrapById(res, wrapper)

    def update_notification(self, id, content=undefined, read=undefined):
        id_arg = parse_arg("id", id)
        content_arg = parse_arg("content", content)
        read_arg = parse_arg("read", read)
        res = self.client.mutation('mutation{updateNotification(%s%s%s){id}}' % (
            id_arg, content_arg, read_arg))["updateNotification"]

        def wrapper(id):
            return Notification(self.client, id)

        return wrapById(res, wrapper)

    def delete_notification(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteNotification(%s)}' % (id_arg))["deleteNotification"]

    def delete_variable(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteVariable(%s)}' % (id_arg))["deleteVariable"]

    def delete_thing(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteThing(%s)}' % (id_arg))["deleteThing"]

    def unpairThing(self, id, reset):
        id_arg = parse_arg("id", id)
        reset_arg = parse_arg("reset", reset)

        return self.client.mutation('mutation{unpairThing(%s%s){id}}' % (id_arg, reset_arg))["unpairThing"]

    def delete_collection(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteCollection(%s)}' % (id_arg))["deleteCollection"]

    def delete_user(self, ):

        return self.client.mutation('mutation{deleteUser()}' % ())["deleteUser"]

    def delete_float_series_node(self, id):
        id_arg = parse_arg("id", id)

        return self.client.mutation('mutation{deleteFloatSeriesNode(%s)}' % (id_arg))["deleteFloatSeriesNode"]

    # def delete_category_series_node(self, id):
    #     id_arg = parse_arg("id", id)

    #     return self.client.mutation('mutation{deleteCategorySeriesNode(%s)}' % (id_arg))["deleteCategorySeriesNode"]
